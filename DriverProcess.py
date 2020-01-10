# -*- coding: utf-8 -*-
from multiprocessing import Process
import time
import _thread as threading    #################################  ONLY NECESSARY IF RECORDING (5)              

import numpy as np

from Terabee3DcamDriver import OpenNiDriver               ###### untouchable ???
from Driver3Dcam import OpenNi2Driver          ###### untouchable ???
from RingBuffer import RingBuffer          ###### untouchable ???
import openni          ###### untouchable ???
#from memory_profiler import profile       ####################### adicionada por mi

class DriverProcess(Process):
    """
    This class wraps a camera driver in a Process object. It also performs
    background and parameters estimation, as well as storing frames in a
    ring buffer and saving them to numpy files.
    """

    def __init__(self, nb_background_frame, driver_fps_window, buffer_size,
                 shared_variables, camera_height):
        """
        This function "unpacks" the shared_variables dictionary and call the
        Process's __init__ function.
        Params:
            nb_background_frame (int): Number of frames used for the first
                background estimation
            driver_fps_window (int): Number of frames used for FPS estimation
            shared_variables (dict): Contains all inter-process variables
        """
        super(DriverProcess, self).__init__()

        # Inter-process communication
        self.cancel = shared_variables["stop_event"]
        self.frame_available = shared_variables["ready_event"]
        self.shared_array = shared_variables["shared_array"]
        self.background_ready = False
        self.recording_trigger = shared_variables["recording_trigger"]
        self.frame_to_record = shared_variables["nb_frame_to_record"]
        self.record_delay = 2

        # Calculated parameters
        self.binarize_threshold = shared_variables["binarized_threshold"]
        self.min_area = shared_variables["min_area"]
        self.detect_threshold = shared_variables["detect_threshold"]
        self.percentile_stdev = 0

        # Parameters
        self.nb_background_frame = nb_background_frame
        self.middle_pixel_value = 0
        self.camera_height = camera_height

        # Variables
        self.buffer_size = buffer_size
        self.ring_buffer = None
        self.background = None
        self.driver_fps_window = driver_fps_window

        """
        OpenNI version selection
        True  ---> OpenNI1
        False ---> OpenNI2
        """
        #OpenNI2 used as default  
        self.openni_version = hasattr(openni,"_openni2")




    def compute_parameters(self):                        ################ SOLO AL PRINCIPIO
        """
        This function tries to estimate good people counting parameters from
        statistics extracted by "compute_std_dev". It estimates binarization
        threshold, minimal area and detection threshold.
        """
        # Auto mode
        # Compute binarization threshold from percentile
        self.binarize_threshold.value = int(
            round(self.percentile_stdev / 16.0 + 5, 0))

        # Compute minimal area from camera height.
        # Divided into two lines, because it is not linear.
        if self.camera_height < 2400:
            min_area = 110
        elif 2400 <= self.camera_height < 2850:
            min_area = -0.0875 * self.camera_height + 320
            min_area = 5 * round(min_area / 5)
        elif 2850 <= self.camera_height <= 3200:
            min_area = -0.0571 * self.camera_height + 223
            min_area = 5 * round(min_area / 5)
        else:
            min_area = 40
        self.min_area.value = int(min_area)
        print('	DRIVERRRR ---> self.min_area.value = ', self.min_area.value)
        # Adapt detect threshold from middle pixel
        # At 2400 => 9, at 3200 => 5
        self.detect_threshold.value = int(-(self.camera_height/266) + 17)

        print("[Driver] Estimated parameters. Min area: {} | " \
              "Detect Threshold: {} | " \
              "Binarize Threshold: {}".format(
                self.min_area.value,
                self.detect_threshold.value,
                self.binarize_threshold.value
                ))

    def shutdown(self):
        """
        This function performs shutdown actions for this class.
        """
        self.cancel.value = True

    def middle_pixel_depth(self, depth_array):
        """
        This function wraps around the driver function that returns the
        center pixel value.
        Params:
            depth_array (np.Array): Frame to extract distance from
        Returns:
             middle pixel distance
        """
        if(self.openni_version==True):
        	return OpenNi2Driver.middle_pixel_depth(depth_array)
        else:
        	return OpenNiDriver.middle_pixel_depth(depth_array)

#    def save_buffer(self):                                              ################ SOLO AL PRINCIPIO
#        """
#        This function saves frames that are in the ring buffer to a
#        compressed numpy file. The number of saved frames depends on
#        frame_to_record and record_delay values.
#
#        """
#        time.sleep(self.record_delay)
#        record_length = int(self.frame_to_record.value +
#                            self.record_delay * 30.0)
#        if record_length > self.buffer_size:
#            record_length = self.buffer_size
#        elif record_length < 1:
#            record_length = 1

#        print("[Driver] Saving last {} frames".format(record_length))
#        try:
#            np.savez(time.strftime("data/detected_%Y-%m-%d_%Hh%Mm%Ss.npz"),
#                 video_data=self.ring_buffer.data[:, :, -record_length:],
#                 background=self.background)
#            print("[Driver] Frames saved !")
#        except (IOError, OSError) as error:
#            print(error)

#    def async_buffer_save(self):
#        """
#        This function wraps the asynchronous implementation of saving frames to
#        a file.
#        """
#        threading.start_new_thread(self.save_buffer, ())


#    @profile
    def run(self):
        """
        This function is the main loop of the Process and is where driver
        data is received. The camera driver is created here as  the
        __init__() function is not run in this Process. This loop waits for
        data from the camera driver and either compute or pass frames to the
        shared buffer to be used by another process.
        """
        if(self.openni_version==True):
        	device = OpenNi2Driver(fps_window=self.driver_fps_window)
        	print('')
        	print('')
        	print('')
        	print('OpenNi2Driver')
        	print('')
        	print('')
        	print('')
        else:
        	device = OpenNiDriver(fps_window=self.driver_fps_window)   
        	print('')
        	print('')
        	print('')
        	print('OpenNiDriver')
        	print('')
        	print('')
        	print('')     	
        self.height = device.height
        self.width = device.width
        self.ring_buffer = RingBuffer(self.height, self.width,
                                      self.buffer_size)
        frame_number = 0
        chacha = device.wait_and_get_depth_frame()
        background_frame = np.ones_like(chacha) * 65535    ####### 65535 is maximum of uint16
        replace_value = int((np.sum(chacha) / np.sum(chacha) != 0)) *66   ######### TO BE CHECKED!
        print("[Driver] Replacing bad values with {}".format(replace_value))

        print("[Driver] Estimating background from {} " \
              "frames".format(self.nb_background_frame))
        mean = np.zeros(chacha.shape)
        stdev = np.zeros(chacha.shape)

        try:
            while not self.cancel.value:
                # We wait for the consumer thread to handle the frame before
                # writing a new one
                while self.frame_available.is_set():
                    pass
                else:
                    frame = device.wait_and_get_depth_frame()
                   # self.ring_buffer.extend(frame)   #################################  ONLY NECESSARY IF RECORDING (1)

                if self.background_ready:
                    # Synchronized write access to shared array
                    # with self.shared_array.get_lock():
                    arr = np.frombuffer(self.shared_array.get_obj(),
                                        dtype='I').reshape(self.height,
                                                           self.width)
                    arr[:] = frame
                    self.frame_available.set()

                else:
                    frame_number = frame_number + 1
         #           print(frame_number)

                    if frame_number <= self.nb_background_frame:
                        mean = mean + frame
                        for j in range(frame.shape[0]):
                            for k in range(frame.shape[1]):
                                if frame[j][k] < background_frame[j][k] and \
                                    frame[j][k] != 0:
                                    background_frame[j][k] = frame[j][k]
                                elif frame[j][k] == 0:
                                    background_frame[j][k] = replace_value
                        if (frame_number == self.nb_background_frame):
                            self.background = background_frame
                            mean = mean / self.nb_background_frame

                    if (frame_number >= self.nb_background_frame) and (frame_number-1 < (self.nb_background_frame*2)):
                        # Compute standard deviation frame
                        stdev += (frame - mean) ** 2
                        if (frame_number == (self.nb_background_frame*2)):
                            stdev = stdev / self.nb_background_frame
                            stdev = np.round(np.sqrt(stdev), 0)
                            # Extract values for parameters estimation
                            self.middle_pixel_value = mean[int(self.height / 2)][
                                int(self.width / 2)]
                            self.percentile_stdev = np.percentile(stdev, 97)





                            self.compute_parameters()
                            arr = np.frombuffer(self.shared_array.get_obj(),
                                                dtype='I').reshape(self.height,
                                                                   self.width)
                            arr[:] = self.background
                            self.background_ready = True
                            print("[Driver] Background ready")
                            self.frame_available.set()
#                        del frame_list  ####################### adicionado por mi

           #     if self.recording_trigger.is_set():  #################################  ONLY NECESSARY IF RECORDING (4)
#                    self.async_buffer_save()    #################################  ONLY NECESSARY IF RECORDING (2)
#                    self.recording_trigger.clear()    #################################  ONLY NECESSARY IF RECORDING (3)
            print("[Driver] Process closing")
            device.shutdown()

        except Exception:
            print("[Driver] Exception in process")
            device.shutdown()
            raise
