# -*- coding: utf-8 -*-
import time


class FpsEstimator(object):
    """
    This class helps estimating the rate at which frames are generated.
    """
    def __init__(self, initial_value=30, window=300, print_prefix=""):   ##### UNITS: initial value: FPS, window: frames
        """
        This is the constructor of the FpsEstimator class.
        Params:
            initial_value (int): Value to initialize the fps estimation
            window (int): Number of ticks between each estimation, can be
                set to zero to disable estimation   
            print_prefix (str): String to display before printing fps value
        """
        # Variables used for fps estimation
        self.last_fps_timestamp = time.time()
        self.fps_window = window
        self.fps_frame_count = 0
        self.fps = initial_value
        self.prefix = print_prefix

    def tick(self):
        """
        This function updates the fps estimation.
        """
        if self.fps_window <= 0:  # Bypass fps computation
            return
        if self.fps_frame_count < self.fps_window:
            self.fps_frame_count += 1
        else:
            current_time = time.time()
            diff = current_time - self.last_fps_timestamp
            self.last_fps_timestamp = current_time

            self.fps = self.fps_frame_count / diff
            self.fps_frame_count = 1
            print("{} FPS: {}".format(self.prefix, round(self.fps, 1)))

    def get_fps(self):
        """Returns the current estimated fps value rounded to the tenth."""
        return round(self.fps, 1)
