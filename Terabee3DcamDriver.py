# -*- coding: utf-8 -*-
from openni import *

import numpy as np

from FpsEstimator import FpsEstimator


class OpenNiDriver(object):
    """
    This class wraps around the OpenNI 1 library driver to easily initialize
    and access data of Terabee 3Dcam.
    """
    def __init__(self, filename=None, fps_window=30):
        """
        This function calls the right OpenNI function to initialize the camera.
        Params:
            filename (str): By default when no filename provided it will
                connect to any OpenNI device. A .oni file can also be provided.
            fps_window (int): Number of frames between each FPS estimation
        """
        self.ctx = Context()
        self.ctx.init()

        # Variables used for fps estimation
        self.fps_estimator = FpsEstimator(30.0, fps_window, "[Driver]")

        # Camera parameters
        self.max_range = 4095
        self.height = 60
        self.width = 80

        if filename is None:

            # Create a depth generator
            self.depth = DepthGenerator()
            self.depth.create(self.ctx)

            # Set it to 30 FPS
            self.depth.fps = 30

            # Start generating
            self.ctx.start_generating_all()
            self.index = 0

        else:

            # Open recording
            self.ctx.open_file_recording(filename)

            self.ctx.start_generating_all()
            self.depth = self.ctx.find_existing_node(NODE_TYPE_DEPTH)

    def read_data(self):
        """
        This function waits for a new frame from the device then converts it
        into an array.
        Returns:
            Depth frame from the camera as an np.Array
        """
        try:
            self.ctx.wait_one_update_all(self.depth)
        except OpenNIError as err:
            print("[Driver] Failed updating data:", err)
        else:

            depth_map = self.depth.get_raw_depth_map()

            depth_array = np.fromstring(depth_map, dtype=np.uint16).reshape((self.height, self.width))

            # Clip values to max range of camera
            depth_array = np.where(depth_array > self.max_range, self.max_range, depth_array)

            self.fps_estimator.tick()
            return depth_array

    @staticmethod
    def middle_pixel_depth(depth_array):
        """
        This function returns the center value of a depth frame from the
        device.
        Params:
            depth_array (np.Array): Frame to extract distance from
        Returns:
             middle pixel distance
        """

        # Get the coordinates of the middle pixel
        x = int(depth_array.shape[0] / 2)
        y = int(depth_array.shape[1] / 2)

        # Get the pixel at these coordinates
        pixel = depth_array[x, y]
        print("[Driver] The middle pixel is %d millimeters away." % pixel)
        return pixel

    def shutdown(self):
        """
        This function performs shutdown actions for the device.
        """
        self.ctx.shutdown()
        return
