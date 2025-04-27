"""Use this as a template of how to make your board compatible with the 
NeuriGUI.
Requirement is that you maintain everything inside the template and only 
add your own steps to the existing ones. This is because the GUI has strict
methods of importing classes and fucntions as well as sharing variables 
between frontend and backend.
"""


from json import dumps
from time import time
from numpy import expand_dims, concatenate, append, array, zeros, reshape
try:
    from io_manager import IOManager
except:
    from .io_manager import IOManager
    

class SamplingUtilsMuseSInteraxon():

    def __init__(self):
        pass # Necessary init function because we call attributes of this class in process_samples()
    

    def message_to_samples(self, lsl_message_eeg, s_chans):
        # -----------------------------------------------------------------
        # Extract samples from board
        # Input
        #   str_message (str) Raw message string coming from board
        #   s_chans     (int) How many channels shall the samples be 
        #               assigned to
        # Default in case of faulty message
        eeg_array       = expand_dims(
            array([0] * s_chans, dtype=float), # Crucial to set float
            axis=1)
        eeg_valid       = False
        #   eeg_array   Numpy array (floats), being channels by samples
        #       (Has to be 2D even if only one channel present [samples x 1])
        #   eeg_valid   Boolean whether workable data or not
        # -----------------------------------------------------------------
        
        eeg_array[:,0] = lsl_message_eeg[0]
        eeg_valid = True
        
        return eeg_array, eeg_valid


    def process_samples(self, transmitter, parameter, shared_buffer,
                     shared_timestamp, gui_running):
        """
        parameter = {
            "baud_rate":    parameter.baud_rate,
            "time_out":     parameter.time_out,
            "port":         parameter.port,
            "start_code":   parameter.start_code, # Start code that boards reads as sign to startt sampling (int)
            "max_chans":    parameter.max_chans, # Specifies how many channels the incoming signals has (int)
            "buffer_length":parameter.buffer_length, # Length of constructed signal buffer (int)
            "buffer_add":   parameter.buffer_add, # Length of padding to avoid filter artifacts  (int)
            "sample_rate":  parameter.sample_rate, # Sampling rate (Hz, int)
            "PGA":          parameter.PGA, # Programmable gain (int)
            "saving_interval": parameter.saving_interval, # how often the data gets written to disk (seconds, int)
            "udp_ip":       parameter.udp_ip, # IP the data shall be forwarded to
            "udp_port":     parameter.udp_port, # Port of signal forwarding
            "set_customsession": parameter.set_customsession, # Whether or not to have a custom output file name (bool)
            "sessionName":  parameter.sessionName, # Custom file name for output (str)
        }"""

        io_manager = IOManager(parameter)
        receiver_eeg, receiver_ppg = io_manager.set_up_lsl_entry_point()

        if parameter["streamed_data_type"] == "EEG":
            receiver = receiver_eeg
        elif parameter["streamed_data_type"] == "PPG":
            receiver = receiver_ppg

        # Prealloate values of loop ---------------------------------------
        start_time          = int(time() * 1000)
        time_stamp_now      = int(time() * 1000) # Do NOT copy from start_time (will generate pointer)
        time_reset          = int(time() * 1000) # Do NOT copy from start_time (will generate pointer)
        sample_count        = int(0)
        
        buffer              = zeros((parameter["max_chans"],
            (parameter["buffer_length"] + parameter["buffer_add"]) * parameter["sample_rate"]))
        time_stamps         = zeros(parameter["buffer_length"] * parameter["sample_rate"], dtype=int)
        pga                 = parameter["PGA"]
        s_chans             = parameter["max_chans"]
        sampling_rate       = parameter["sample_rate"]
        saving_interval     = parameter["saving_interval"] * parameter["sample_rate"]
        update_buffer       = zeros((buffer.shape[0], buffer.shape[1]+1))
        update_times        = zeros((buffer.shape[1]+1), dtype=int)

        # Preallocate json relay message and relay connection
        relay_array         = io_manager.build_standard_relay_message(parameter["max_chans"])
        udp_ip              = parameter["udp_ip"]
        udp_port            = parameter["udp_port"]
            
        while gui_running.value == 1:
            
            # =========================================================
            # ========= B O A R D   S P E C I F I C   P A R T =========
            # =========================================================
            raw_message_eeg        = receiver.pull_sample()

            # TODO: Circumvent fact that PPG is sampled at 64 Hz and
            # slows down EEG sampling which is sending at 256 Hz.
            # raw_message_ppg        = receiver_ppg.pull_sample()

            # TODO: Adapt message_to_samples() in order to convert
            # raw_message string into numpy array of samples
            buffer_in, valid_eeg    = self.message_to_samples(raw_message_eeg, s_chans)

            if not valid_eeg:
                # TODO: Implement an interpolation system
                continue                
            # =========================================================
            # =========================================================
            # =========================================================

            # Standard set of procedures from here on: You should not
            # require any additional changes from here

            # Current timestamp -------------------------------------------
            time_stamp_now          = int(raw_message_eeg[1] / 1000) - start_time
            # This will generate unchanged time_stamps for all samples of 
            # the incoming buffer (= 10 in case of bluetooth), but that is
            # not a problem

            sample_count        = sample_count + 1
            
            sample              = buffer_in[:, 0]

            for iSample in range(s_chans):
                relay_array["".join(["c", str(iSample+1)])] = str(sample[iSample])

            update_buffer       = concatenate((buffer, expand_dims(sample, 1)), axis=1)
            update_times        = append(time_stamps, time_stamp_now)

            # Build new buffer and timestamp arrays
            buffer              = update_buffer[:, 1:]
            time_stamps         = update_times[1:]

            # Make data available for downstream programs
            transmitter.sendto(bytes(dumps(relay_array), "utf-8"), (udp_ip, udp_port))

            # Update shared memory allocations for frontend
            shared_buffer[:] = reshape(buffer, buffer.size) # Has left edge for filtering
            shared_timestamp.value = time_stamp_now

            # Write out samples to file -----------------------------------
            if sample_count == saving_interval:

                io_manager.calc_sample_rate(time_stamp_now, time_reset, 
                                    sampling_rate, time_stamps)

                io_manager.master_write_data(buffer, time_stamps, 
                    saving_interval)
                sample_count        = 0
                time_reset          = time_stamp_now

        return