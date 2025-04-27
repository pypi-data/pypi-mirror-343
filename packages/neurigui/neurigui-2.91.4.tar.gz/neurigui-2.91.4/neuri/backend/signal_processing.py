from scipy.signal import butter, lfilter_zi, lfilter, hilbert
from numpy import zeros, pad, abs


class Processing():

    def __init__(self, parameters):

        self.pm                 = parameters
        self.prepare_filters()


    def prepare_filters(self):

        # Bandpass filters
        # -----------------------------------------------------------------
        self.b_detrend, self.a_detrend          = butter(
            self.pm.filter_order, self.pm.frequency_bands["Whole"][0],
            btype='highpass', fs=self.pm.sample_rate)
        self.b_slow, self.a_slow                = butter(
            self.pm.filter_order, self.pm.frequency_bands["Slow"],
            btype='bandpass', fs=self.pm.sample_rate)
        
        if self.pm.streamed_data_type == "EEG":
            self.b_wholerange, self.a_wholerange    = butter(
                self.pm.filter_order, self.pm.frequency_bands["Whole"],
                btype='bandpass', fs=self.pm.sample_rate)
            self.b_sleep, self.a_sleep              = butter(
                self.pm.filter_order, self.pm.frequency_bands["Sleep"],
                btype='bandpass', fs=self.pm.sample_rate)
            self.b_theta, self.a_theta              = butter(
                self.pm.filter_order, self.pm.frequency_bands["Theta"],
                btype='bandpass', fs=self.pm.sample_rate)
            self.b_notch, self.a_notch              = butter(
                self.pm.filter_order, self.pm.frequency_bands["LineNoise"],
                btype='bandstop', fs=self.pm.sample_rate)
            self.b_notch60, self.a_notch60          = butter(
                self.pm.filter_order, self.pm.frequency_bands["LineNoise60"],
                btype='bandstop', fs=self.pm.sample_rate)

        # Determine padding length for signal filtering
        # -----------------------------------------------------------------
        default_pad     = 6 * max(len(self.a_detrend), len(self.b_detrend))
        if default_pad > self.pm.buffer_length * self.pm.sample_rate/10-1:
            self.padlen = int(default_pad) # Scipy expects int
        else:
            self.padlen = int(self.pm.buffer_length*self.pm.sample_rate/10-1) # Scipy expects int


    def filter_signal(self, signal, b, a):
        # =================================================================
        # Input:
        #   signal              Numpy 1D array [samples]
        # Output:
        #   signal_filtered[0]  1D numpy array of filtered signal where 
        #                       first sample is 0
        # =================================================================
        padded_signal   = pad(signal, (self.padlen, 0), 'symmetric')
        init_state      = lfilter_zi(b, a) # 1st sample --> 0
        signal_filtered = lfilter(b, a, padded_signal, 
            zi=init_state*padded_signal[0])
        signal_filtered = signal_filtered[0][self.padlen:]
        return signal_filtered


    def extract_envelope(self, signal):
        v_hilbert       = signal
        for iChan in range(signal.shape[0]):
            # padded_signal   = np.pad(signal[iChan,], (self.padlen, self.padlen), 'symmetric')
            # hilbert[iChan,] = np.abs(scipy.signal.hilbert(padded_signal))[self.padlen:-self.padlen]
            v_hilbert[iChan,] = abs(hilbert(signal[iChan,]))
        return v_hilbert


    def downsample(self, buffer, s_down):
        # =================================================================
        # Input:
        #   buffer              Numpy array [channels x samples]
        # Output:
        #   downsamples_buffer  Numpy array of downsampled signal, same  
        #                       dimensions as input buffer
        # =================================================================

        downsampled_signal  = zeros((buffer.shape[0], int(buffer.shape[1]/s_down)))
        idx_retain = range(0, buffer.shape[1], s_down)
        for iChan in range(self.pm.max_chans):
            # downsampled_signal[iChan,] = scipy.signal.decimate(buffer[iChan,], s_down)
            downsampled_signal[iChan,] = buffer[iChan,idx_retain]

        return downsampled_signal


    def prepare_buffer(self, buffer, bSB, aSB, bPB, aPB):
        # =================================================================
        # Input:
        #   buffer              Numpy array [channels x samples]
        #   bSB, aSB            Filter coefficients as put out by 
        #                       scipy.signal.butter (Stopband)
        #   bPB, aPB            Filter coefficients as put out by 
        #                       scipy.signal.butter (Passband)
        # Output:
        #   filtered_buffer     Numpy array of filtered signal, same  
        #                       dimensions as input buffer
        # =================================================================
        x_shape             = buffer.shape

        noise_free_signal   = zeros(x_shape)
        filtered_buffer     = zeros(x_shape)
        for iChan in range(x_shape[0]):

            # Reject ambiant electrical noise (at 50 Hz)
            # -------------------------------------------------------------
            if all(bSB != None):
                noise_free_signal[iChan,] = self.filter_signal(
                    buffer[iChan,], bSB, aSB)
            else:
                noise_free_signal[iChan,] = buffer[iChan,]

            # Extract useful frequency range
            # -------------------------------------------------------------
            if all(bPB != None):
                filtered_buffer[iChan,] = self.filter_signal(
                    noise_free_signal[iChan,], bPB, aPB)
            else:
                filtered_buffer[iChan,] = noise_free_signal[iChan,]

        return filtered_buffer