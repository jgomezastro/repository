# -*- coding: utf-8 -*-
from multiprocessing import Process
import time
import _thread as threading

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

    def background_estimation(self, frame_list):                        ################ SOLO AL PRINCIPIO
        """
        This function estimates the background by taking the minimum value
        seen for each pixel in a set of frames. It replaces zero-values by
        the mean value of all frames.
        Params:
            frame_list (list): List of frames to estimate the background from
        Returns:
            Estimated background as an np.Array()
        """
        background_frame = np.ones_like(frame_list[0]) * 65535    ####### 65535 is maximum of uint16
        replace_value = int(np.sum(frame_list[0]) / np.sum(frame_list[0] != 0))    ######### TO BE CHECKED!
#        replace_value = int(np.sum(frame_list[0]) / len(frame_list[0] != 0))       ######### CORRECT????
        print("[Driver] Replacing bad values with {}".format(replace_value))
        for i in range(self.nb_background_frame):
            for j in range(frame_list[0].shape[0]):
                for k in range(frame_list[0].shape[1]):
                    if frame_list[i][j][k] < background_frame[j][k] and \
                            frame_list[i][j][k] != 0:
                        background_frame[j][k] = frame_list[i][j][k]
                    elif frame_list[i][j][k] == 0:
                        background_frame[j][k] = replace_value
        return background_frame

    def compute_std_dev(self, frame_list):                        ################ SOLO AL PRINCIPIO
        """
        This function extracts statistics from a list of frames. Extracts
        middle pixel average value and 95th percentile.
        Params:
            frame_list (list): List of frames to perform statistics on
        """
        # Compute mean frame
        mean = np.zeros(frame_list[0].shape)
        for i in range(len(frame_list)):
            mean += frame_list[i]
        mean = mean / len(frame_list)

        # Compute standard deviation frame
        stdev = np.zeros(frame_list[0].shape)
        for i in range(len(frame_list)):
            stdev += (frame_list[i] - mean) ** 2
        stdev = stdev / len(frame_list)
        stdev = np.round(np.sqrt(stdev), 0)

        # Extract values for parameters estimation
        self.middle_pixel_value = mean[int(self.height / 2)][
            int(self.width / 2)]
        self.percentile_stdev = np.percentile(stdev, 97)
        print('	DRIVERRRR ---> self.middle_pixel_value = ', self.middle_pixel_value)
        print('	DRIVERRRR ---> self.percentile_stdev = ', self.percentile_stdev)

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

    def save_buffer(self):                                              ################ SOLO AL PRINCIPIO
        """
        This function saves frames that are in the ring buffer to a
        compressed numpy file. The number of saved frames depends on
        frame_to_record and record_delay values.

        """
        time.sleep(self.record_delay)
        record_length = int(self.frame_to_record.value +
                            self.record_delay * 30.0)
        if record_length > self.buffer_size:
            record_length = self.buffer_size
        elif record_length < 1:
            record_length = 1

        print("[Driver] Saving last {} frames".format(record_length))
        try:
            np.savez(time.strftime("data/detected_%Y-%m-%d_%Hh%Mm%Ss.npz"),
                 video_data=self.ring_buffer.data[:, :, -record_length:],
                 background=self.background)
            print("[Driver] Frames saved !")
        except (IOError, OSError) as error:
            print(error)

    def async_buffer_save(self):
        """
        This function wraps the asynchronous implementation of saving frames to
        a file.
        """
        threading.start_new_thread(self.save_buffer, ())


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
        frame_list = []

        try:
            while not self.cancel.value:
                # We wait for the consumer thread to handle the frame before
                # writing a new one
                while self.frame_available.is_set():
                    pass
                else:
                    frame = device.wait_and_get_depth_frame()
                    self.ring_buffer.extend(frame)

                if self.background_ready:
                    # Synchronized write access to shared array
                    # with self.shared_array.get_lock():
                    arr = np.frombuffer(self.shared_array.get_obj(),
                                        dtype='I').reshape(self.height,
                                                           self.width)
                    arr[:] = frame
                    self.frame_available.set()

                else:
                    frame_list.append(frame)

                    if len(frame_list) >= self.nb_background_frame:
                        # Estimate background
                        print("[Driver] Estimating background from {} " \
                              "frames".format(self.nb_background_frame))
                        arr = np.frombuffer(self.shared_array.get_obj(),
                                            dtype='I').reshape(self.height,
                                                               self.width)
                        self.background = self.background_estimation(
                            frame_list)
                        self.compute_std_dev(frame_list)
                        self.compute_parameters()
                        arr[:] = self.background
                        self.background_ready = True
                        print("[Driver] Background ready")
                        self.frame_available.set()
#                        del frame_list  ####################### adicionado por mi

                if self.recording_trigger.is_set():
                    self.async_buffer_save()
                    self.recording_trigger.clear()
            print("[Driver] Process closing")
            device.shutdown()

        except Exception:
            print("[Driver] Exception in process")
            device.shutdown()
            raise
