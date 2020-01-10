#!/usr/bin/python3

from openni import openni2
from openni import _openni2 as c_api
import ctypes
import numpy as np
from FpsEstimator import FpsEstimator
import platform  ####### Specific platforms listed alphabetically, with Linux included in the Unix section.
from multiprocessing import Event
#from memory_profiler import profile       ####################### adicionada por mi

class OpenNi2Driver:
#    @profile
    def __init__(self, fps_window=30):
        # Camera parameters
        self.max_range = 4095
        self.height = 60
        self.width = 80
        self.index = 0

         # Variables used for fps estimation
        self.depth_fps_estimator = FpsEstimator(30.0, fps_window, "[Driver] Depth stream")
        self.ir_fps_estimator = FpsEstimator(30.0, fps_window, "[Driver] IR stream")
        
        #Connect and Open Device
        if platform.system() == "Windows":
            openni2.initialize("C:/Program Files/OpenNI2/Redist") #specify path for Redist
        else:
            openni2.initialize()        #######################################  adds 45.5 MiB 
        self.dev = openni2.Device.open_any()             #######################################  adds 6.7 MiB
        self.serial_number = (self.dev.get_property(c_api.ONI_DEVICE_PROPERTY_SERIAL_NUMBER, (ctypes.c_char * 100)).value).decode('utf-8')

        #Start IR Streaming
        # self.ir_frame = np.zeros((self.height, self.width))
        # self.ir_stream = self.dev.create_ir_stream()
        # self.ir_frame_ready = Event()
        # self.ir_stream.register_new_frame_listener(self.ir_frame_callback)
        # self.ir_stream.start()

        #Start Depth Streaming
        self.depth_frame = np.zeros((self.height, self.width))
        self.depth_stream = self.dev.create_depth_stream()
        self.depth_frame_ready = Event()
        self.depth_stream.register_new_frame_listener(self.depth_frame_callback)
        self.depth_stream.start()
#    @profile
    def ir_frame_callback(self, stream):
        frame = stream.read_frame()
        ir_frame = frame.get_buffer_as_uint16()

        #Converting array into frame and frame update
        self.ir_frame = np.asarray(ir_frame).reshape((self.height, self.width))
        self.ir_frame_ready.set()
        self.ir_fps_estimator.tick()
#    @profile
    def depth_frame_callback(self, stream):
        frame = stream.read_frame()
        depth_frame = frame.get_buffer_as_uint16()
        buffer_copy = []
        buffer_copy[:] = depth_frame

        #Converting array into frame and frame update
        self.depth_frame = np.asarray(buffer_copy).reshape((self.height, self.width))
        self.depth_frame = np.where(self.depth_frame > self.max_range, self.max_range, self.depth_frame)
        self.depth_frame_ready.set()
        self.depth_fps_estimator.tick()
#    @profile
    def wait_and_get_ir_frame(self) :
        self.ir_frame_ready.wait(5)
        self.ir_frame_ready.clear()
        return self.ir_frame
#    @profile
    def wait_and_get_depth_frame(self):
        self.depth_frame_ready.wait(5)
        self.depth_frame_ready.clear()
        return self.depth_frame
#    @profile
    @staticmethod
    def middle_pixel_depth(depth_array):

        # Get the coordinates of the middle pixel
        x = int(depth_array.shape[0] / 2)
        y = int(depth_array.shape[1] / 2)

        # Get the pixel at these coordinates
        pixel = depth_array[x, y]
        print("[Driver] The middle pixel is %d millimeters away." % pixel)
        return pixel
#    @profile
    def shutdown(self):
        #Stop and Release
        #self.ir_stream.stop()
        self.depth_stream.stop()
        openni2.unload()
        return
