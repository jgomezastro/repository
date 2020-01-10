# -*- coding: utf-8 -*-
import time
from multiprocessing import Process

import numpy as np


class FileReaderProcess(Process):
    """
    This class wraps a file reader in a Process object. This class follows
    the same behaviour as a camera driver process to be compatible with the
    MultiplePeopleCounter class.
    """

    def __init__(self, filename, rate, shared_variables):
        """
        This function "unpacks" the shared_variables dictionary and
        call the Process's __init__ function.
        Params:
            filename (str): Path of the file to read
            rate (int): Rate of the playback in Hz (frames per second)
            shared_variables (dict): Contains all inter-process variables
        """
        super(FileReaderProcess, self).__init__()

        # Variables
        self.filename = filename
        self.frame_buffer = []
        self.background = []
        self.index = -1
        self.last_time_called = 0.0
        self.playback_freq = rate

        # Inter-process communication
        self.cancel = shared_variables["stop_event"]
        self.frame_available = shared_variables["ready_event"]
        self.shared_array = shared_variables["shared_array"]

    def shutdown(self):
        """
        This function performs shutdown actions for this class.
        """
        self.cancel.value = True

    def middle_pixel_depth(self, depth_array):
        """
        This function wraps around the frame producer function that returns the
        center pixel value.
        Params:
            depth_array (np.Array): Frame to extract distance from
        Returns:
             middle pixel distance as int
        """
        # Get the coordinates of the middle pixel
        x = int(depth_array.shape[0] / 2)
        y = int(depth_array.shape[1] / 2)

        # Get the pixel at these coordinates
        pixel = depth_array[x, y]
        print("[Driver] The middle pixel is %d millimeters away." % pixel)
        return pixel

    def throttle(self):
        """
        This function waits for the right amount of time to match the playback
        rate.
        """
        min_delay = 1.0 / float(self.playback_freq)

        elapsed = time.time() - self.last_time_called
        to_be_waited = min_delay - elapsed

        if to_be_waited > 0:
            time.sleep(to_be_waited)

        self.last_time_called = time.time()

    def next_frame(self):
        """
        This functions deals with getting either the background or the next
        frame in the buffer.
        """
        if self.index < 0:
            current_frame = self.background
        else:
            current_frame = self.frame_buffer[:, :, self.index]
        self.index += 1

        return current_frame

    def run(self):
        """
        This function is the main loop of the Process and is where the data
        is loaded from the file. Here, the loop is throttled to write frames
        to a shared array at a constant playback rate.
        """
        try:
            file_data = np.load(self.filename)
            self.background = file_data['background']
            self.frame_buffer = file_data['video_data']

            while not self.cancel.value:
                # We wait for the consumer thread to handle the frame before
                # writing a new one
                while self.frame_available.is_set():
                    pass
                else:
                    frame = self.next_frame()

                arr = np.frombuffer(self.shared_array.get_obj(),
                                    dtype='I').reshape(60, 80)
                arr[:] = frame
                self.frame_available.set()
                self.throttle()

                if self.index == self.frame_buffer.shape[2]:
                    break

            print("[File reader] Reached end of file {}".format(self.filename))

        except IOError:
            print("[File reader] Error while reading file {}".format(
                self.filename))

        except Exception:
            print("[File reader] File reader process exception")
            raise
