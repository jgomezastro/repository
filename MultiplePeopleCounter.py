# -*- coding: utf-8 -*-

from time import time as timee
from time import strftime
from datetime import time as ttime
from datetime import timedelta
from datetime import datetime
from datetime import date
from csv import writer as writerr
from csv import reader as readerr
from contourAreaa import contourAreaa
from Polygontestpoint import Polygontestpoint
from openingg import openingg
from closingg import closingg
from min_contourss import min_contourss
from Polygoncentroid import Polygoncentroid
#from Drawfilledcontour import Drawfilledcontour
from Drawfilledcontour7 import Drawfilledcontour
from FindContourss import FindContourss
#from Drawfilledcontour5 import Drawfilledcontour
from collections import deque    ####### collections ---> specialized container datatypes
                                 ####### deque       ---> list-like container with fast appends and pops on either end
                                 #######                  Returns a new deque object initialized left-to-right 
                                 #######                  (using append()) with data from iterable. If iterable is not 
                                 #######                  specified, the new deque is empty.
                                 #######                    Deques are a generalization of stacks and queues (the name 
                                 #######                    is pronounced “deck” and is short for “double-ended queue”).
                                 #######                    Deques support thread-safe, memory efficient appends and pops
                                 #######                    from either side of the deque with approximately the same 
                                 #######                    O(1) performance in either direction.
                                 #######                    Though list objects support similar operations, they are 
                                 #######                    optimized for fast fixed-length operations and incur O(n) 
                                 #######                    memory movement costs for pop(0) and insert(0, v) operations 
                                 #######                    which change both the size and position of the underlying 
                                 #######                    data representation.

import multiprocessing as mp     ####### multiprocessing: a package that supports spawning processes using an API similar
                                 #######                  to the threading module. The multiprocessing package offers both 
                                 #######                  local and remote concurrency, effectively side-stepping the Global
                                 #######                  Interpreter Lock by using subprocesses instead of threads. Due to
                                 #######                  this, the multiprocessing module allows the programmer to fully
                                 #######                  leverage multiple processors on a given machine. It runs on both 
                                 #######                  Unix and Windows.
                                 #######                  The multiprocessing module also introduces APIs which do not have 
                                 #######                  analogs in the threading module. A prime example of this is the 
                                 #######                  Pool object which offers a convenient means of parallelizing the 
                                 #######                  execution of a function across multiple input values, distributing 
                                 #######                  the input data across processes (data parallelism).

from _thread import start_new_thread      ####### _thread: This module provides low-level primitives for working with multiple threads
                                 #######          (also called light-weight processes or tasks) — multiple threads of control 
                                 #######          sharing their global data space. For synchronization, simple locks (also 
                                 #######          called mutexes or binary semaphores) are provided. The threading module 
                                 #######          provides an easier to use and higher-level threading API built on top of 
                                 #######          this module.

from requests import get                 ####### requests: Make a request to a web page, and print the response text:
from requests import exceptions

from glob import glob                      ####### to locate files*
from os import path                        ####### to locate files*

#import numpy as np               ####### NumPy is the fundamental package for scientific computing with Python. It contains 
from numpy import zeros_like
from numpy import zeros
from numpy import ones
from numpy import array
from numpy import uint8
from numpy import where
from numpy import prod
from numpy import nanmin
from numpy import nan
from numpy import frombuffer
from numpy import copy
from numpy import squeeze
from numpy import concatenate
from numpy import float as floatt
from numpy import max as maxx
                                 ####### among other things:
                                 ####### * a powerful N-dimensional array object
                                 ####### * a powerful N-dimensional array objectsophisticated (broadcasting) functions
                                 ####### * a powerful N-dimensional array objecttools for integrating C/C++ and Fortran code
                                 ####### * a powerful N-dimensional array objectuseful linear algebra, Fourier transform, and
                                 ####### * random number capabilities
                                 ####### Besides its obvious scientific uses, NumPy can also be used as an efficient
                                 ####### multi-dimensional container of generic data. Arbitrary data-types can be defined. 
                                 ####### This allows NumPy to seamlessly and speedily integrate with a wide variety of 
                                 ####### databases.

#import cv2                       ####### opencv2
from cv2 import FONT_HERSHEY_SIMPLEX
from cv2 import morphologyEx
from cv2 import MORPH_OPEN
from cv2 import MORPH_CLOSE
from cv2 import findContours
from cv2 import RETR_EXTERNAL
from cv2 import CHAIN_APPROX_SIMPLE
from cv2 import contourArea
from cv2 import drawContours
from cv2 import minMaxLoc
from cv2 import pointPolygonTest
from cv2 import cvtColor
from cv2 import COLOR_GRAY2RGB
from cv2 import putText
from cv2 import LINE_AA
from cv2 import LINE_8
from cv2 import EVENT_FLAG_CTRLKEY
from cv2 import boundingRect
from cv2 import rectangle
from cv2 import circle
from cv2 import line as linee
from cv2 import waitKey
from cv2 import setMouseCallback
from cv2 import EVENT_LBUTTONUP
from cv2 import EVENT_FLAG_CTRLKEY
from cv2 import namedWindow
from cv2 import WINDOW_NORMAL
from cv2 import moveWindow
from cv2 import imshow
from cv2 import destroyAllWindows


from Person import TrackedObject             ###### 
from DriverProcess import DriverProcess          ###### parameter computation or estimation inside, initial background
from FileReaderProcess import FileReaderProcess            ###### 
from MultiplePeopleCounterConfig import MultiplePeopleCounterConfig     #### 
import Trackers          ###### touchable 
import Counters          ###### touchable
from FpsEstimator import FpsEstimator          ###### 
#from memory_profiler import profile       ####################### adicionada por mi
#from guppy import hpy


__version__ = "2.0.1"


class WinName(object):
    """
    This class enumerates the different names of windows.
    """
    BGD = "Background"
    VIS = "Visualization"
    BIN = "Binarized"
    DET = "Detection"


class MultiplePeopleCounter(object):
    """
    This is the main class of people counting, it contains the depth image
    processing pipeline, visualization and internet functions. It can be use
    with a camera or a numpy file containing frames.

    """
#    @profile
    def __init__(self, filename=None, playback_rate=30.0):
        # Camera settings
        """
        Here we define all default values of parameters, instantiate shared
        variables, files, drivers and processes.
        Params:
            filename (str): Numpy file to load
            playback_rate (int): Rate at which the data will be played in Hz
        """
        self.height = 60
        self.width = 80
        self.h_flip = False         
        self.v_flip = False       
        self.rotate_90 = False

        # General variables
        self.line_edit_mode = False      
        self.first_click = False     
        self.font = FONT_HERSHEY_SIMPLEX
        self.max_p_age = 10
        self.in_area_points = array([[0, int(self.height / 2)],
                                        [self.width-1, int(self.height/2)],
                                        [self.width-1, self.height-1],
                                        [0, self.height-1]])
        self.scaling_factor = 4095.0     ##########  mm 
        self.max_uint8 = 255         ######### int8
        self.middle_pixel_check = False
        self.camera_height = 2500
        self.exclusion_height = 600

        # Variables used for fps estimation
        self.fps_window = 60        ######### number of frames used to estimate number of frames per second

        # Algorithm parameters
        self.min_area = 50
        self.nb_background_frame = 90
        self.detect_threshold = 25  # 25*16 = 400mm side of a head     ########### units: 8bits
        self.reversed_counting_direction = False
        self.max_people_in_view = 8
        self.binarize_threshold = 30       ########### units: 8bits
        self.matching_ratio = 1.3  ######### A parameter for the greedy part  TBD???
        self.max_tracking_distance = 12
        self.tracker_type = Trackers.TrackerType.PROXIMITY   #contours for proximity when tracking
        self.auto_compute_params = True      ######### tRUE= taken from DP;  False= taken from conf file

        # Windows parameters
        self.display_background = False
        self.display_binarized = False
        self.display_detected = False
        self.display_visualization = True
        self.visualization_colour = (0, 300, 255)       ######### BGR or BRG  to be searched

        # Recording events
        self.record_on_counting_event = False
        self.buffer_size = 1800  # Size of the ring buffer 1800 is 1min        ######### last minute remembering

        # Data pushing to internet
        self.push_count_to_internet = False
        self.push_url = "http://iot.teraranger.com/iot/push_counts?sensor_id" \
                        "={}&count_in={}&count_out={} "
        self.sensor_id = 1
        self.push_interval = 60        ######### sec
        self.last_push = timee()

        # Logging parameters
        self.log_counting_events = True
        self.reset_hour = ttime(00, 00)
        self.next_reset = datetime.today()
        self.outfile = None
        self.restore_counts = True

        # Background parameters
        self.background = zeros((self.height, self.width), uint8)
        self.background_intermediate = ones((self.height, self.width),
                                               floatt) * 255
        self.bg_frame_interval = 3  # Frame interval of background update
        self.bg_threshold = 10  # Minimal difference needed to tigger          ######### btw [0,255]
        # background update
        self.bg_growth_rate = 0.003  # Rate at which an object will be taken
        # into the background               ######### related to time, distance per frame (or sec TBD)
        self.bg_decay_rate = 0.15  # Rate at which an object will be removed
        # from the background                ######### related to time, distance per frame (or sec TBD)

        # Moving Average parameters
        self.filtered_array = []
        self.window_size = 2
        self.sum = 0
        self.__q = deque([])
        self.val = 0

        # Iterations number for the opening morphology, for binarize
        self.iterations_number = 1          ######### INCREASE IF MANY NOISE

        # Bilateral Filter parameters USUALLY NOT USED
        self.kernel = 5  # diameter of each pixel neighborhood that is used
        # during filtering                  ######### PIXELS
        self.depth_difference = 30  # difference of colour that will be        UNITS??????????????????????????
        # checked in the area to be mixed                   ######### 0,255
        self.area_checked = 30  # how far from the distance neighborhood we     UNITS??????????????????????????
        # check for mixing.
        self.activate_filter = False

        # Load config file
        # WARNING: Any param set after this will override its value in the
        # config file
        self.first_reset = True
        self.config_filename = "config.yaml"
        self.load_config()


        # Initialize fps estimator
        self.fps_estimator = FpsEstimator(30.0, self.fps_window, "[Counter]")

        # Initialize the right tracker
        if self.tracker_type == Trackers.TrackerType.GREEDY:
            self.tracker = Trackers.GreedyTracker(self.max_p_age,
                                                  self.track_lost_callback,
                                                  self.matching_ratio)
        elif self.tracker_type == Trackers.TrackerType.PROXIMITY:
            self.tracker = Trackers.ProximityTracker(self.max_p_age,
                                                     self.track_lost_callback,
                                                     self.max_tracking_distance)

        # Initialize the counter
        self.counter = Counters.AreaCounter(self.in_area_points,
                                            self.reversed_counting_direction)
        self.tracker.register_on_track_lost_callback(
            self.counter.get_final_count)
        self.counter.register_in_events_callback(self.count_in)
        self.counter.register_out_event_callback(self.count_out)



        # Create shared variables and processes
        self.shared_array_dim = (self.height, self.width)
        self.shared_array = mp.Array('I', int(prod(self.shared_array_dim)))
        self.stop = mp.Value('i', False)
        self.device_ready = mp.Event()
        self.recording_trigger_event = mp.Event()
        self.nb_frame_to_record = mp.Value('I', 0)

        self.shared_variables = {
            "shared_array": self.shared_array,
            "ready_event": self.device_ready,
            "stop_event": self.stop,
            "recording_trigger": self.recording_trigger_event,
            "nb_frame_to_record": self.nb_frame_to_record,       ######### RELATED TO RING BUFFER, LAST
            "binarized_threshold": mp.Value('I', 0),
            "detect_threshold": mp.Value('I', 0),
            "min_area": mp.Value('I', 0),
        }



        if filename is None:
            self.playback = False

            self.driver = DriverProcess(self.nb_background_frame,
                                        self.fps_window, self.buffer_size,
                                        self.shared_variables,
                                        self.camera_height)
            self.driver.start()

            if self.log_counting_events:
                self.init_log_file()

        else:
            self.driver = FileReaderProcess(filename, playback_rate,
                                            self.shared_variables)
            self.driver.start()

            self.playback = True

        self.pause = False
        self.get_once = False


        # Recover last IN/OUT in case of a crash or reboot
        data = self.read_count_in_log()
        try:
            self.counter.count_in = int(data[-1][2])
            self.counter.count_out = int(data[-1][3])
        except ValueError:
            print("Couldn't recover last count")
        except IndexError:
            print("No previous data today")
        print("last_in {} last_out {}".format(self.counter.count_in, self.counter.count_out))

#    @profile
    def get_count_in(self):
        """Returns number of entries"""
        return self.counter.count_in
#    @profile
    def get_count_out(self):
        """Returns number of exits"""
        return self.counter.count_out
#    @profile
    def load_config(self):
        """
        This function instantiates a MultiplePeopleCounterConfig from a
        yaml file.

        """
        print("[Counter] Loading config from {}".format(self.config_filename))
        self.cfg = MultiplePeopleCounterConfig(self.config_filename)
        self.map_config()
        self.next_reset.replace(hour=self.reset_hour.hour,
                                minute=self.reset_hour.minute)
#    @profile
    def map_config(self):
        """
        This function will map class attributes to one attribute inside the
        MultiplePeopleCounterConfig object.
        """
        # Here we map params of the config object to the counter object with
        # a lambda function if any conversion is necessary
        self.map_config_params("reversed_counting_direction",
                               "counting_params_user.reversed_counting_direction")
        self.map_config_params("camera_height",
                               "counting_params_user.camera_height")
        self.map_config_params("in_area_points",
                               "counting_params_user.in_area",
                               lambda counter, value: array(value))
        self.map_config_params("exclusion_height",
                               "counting_params_user.exclusion_height")

        # Parameters that are gonna be fix
        self.map_config_params("max_p_age",
                               "counting_params_fixed.maximum_age")
        self.map_config_params("max_tracking_distance",
                               "counting_params_fixed.max_tracking_distance_px")

        # Parameters that are gonna be calculated
        self.map_config_params("auto_compute_params",
                               "counting_params_calculated.auto")
        self.map_config_params("detect_threshold",
                               "counting_params_calculated.detect_threshold")
        self.map_config_params("min_area",
                               "counting_params_calculated.min_area")
        self.map_config_params("binarize_threshold",
                               "counting_params_calculated.binarize_threshold")

        # Background parameters
        self.map_config_params("nb_background_frame",
                               "background.nb_background_frame")
        self.map_config_params("bg_frame_interval",
                               "background.background_frame_interval")

        # Noise filtering parameters
        self.map_config_params("window_size",
                               "noise_filter_params.window_size")
        self.map_config_params("iterations_number",
                               "noise_filter_params.iterations_number")
        self.map_config_params("activate_filter",
                               "noise_filter_params.activate_filter")
        self.map_config_params("kernel", "noise_filter_params.kernel")
        self.map_config_params("depth_difference",
                               "noise_filter_params.depth_difference")
        self.map_config_params("area_checked",
                               "noise_filter_params.area_checked")

        self.map_config_params("display_background",
                               "display_windows.background")
        self.map_config_params("display_binarized",
                               "display_windows.binarized")
        self.map_config_params("display_detected", "display_windows.detected")
        self.map_config_params("display_visualization",
                               "display_windows.visualization")

        self.map_config_params("push_count_to_internet",
                               "pushing_data.enabled")
        self.map_config_params("push_url", "pushing_data.push_url")
        self.map_config_params("sensor_id", "pushing_data.sensor_id")
        self.map_config_params("push_interval", "pushing_data.push_interval")

        self.map_config_params("fps_window", "logging.fps_window")
        self.map_config_params("reset_hour",
                               "logging.reset_hour",
                               lambda counter, value:
                               datetime.strptime(value,
                                                          "%H:%M").time())
        self.map_config_params("restore_counts",
                               "logging.restore_counts")

        self.map_config_params("record_on_counting_event",
                               "record_frames.on_counting_event")

        self.map_config_params("middle_pixel_check",
                               "miscs.middle_pixel_check")
#    @profile
    def map_config_params(self, attr, cfg_attr,
                          f=lambda counter, value: value):
        """
        This function will try to set a class attribute with one in the
        config based on their names. It will also apply a function f to this
        value.
        Params:
            attr (str): Name of the class attibute to map
            cfg_attr (str): Name of config attribute to map
            f (lambda): Function to be applied on the value before mapping
        """
        value = self.cfg.rgetattr(cfg_attr)
        if value is not None:
            if hasattr(self, attr):
                setattr(self, attr, f(self, value))
            else:
                print("[Counter Warning] Trying to map value to unexistent " \
                      "attribute {}".format(attr))
        else:
            print("[Counter Warning] Missing parameter \"{}\" in config " \
                  "file. Default value will be used".format(cfg_attr))
#    @profile
    def init_log_file(self):
        """
        This function creates a csv file in the /logs folder.
        """
        filename = strftime("logs/counting_results_%Y-%m-%d.csv")
        try:
            self.outfile = open(filename, "a+")
            self.csvfile = writerr(self.outfile, dialect='excel')
            self.csvfile.writerow(["Time", "In", "Out"])
            print("[Counter] Log file successfully created")
        except (IOError, OSError) as error:
            print("[Counter] Couldn't create file: {}".format(filename))
            print(error)
            raise
#    @profile
    def close_log_file(self):
        """
        This function closes the log file. It will write the count one last
        time before closing.
        """
        if self.outfile is not None:
            self.write_count_to_log()
            self.outfile.close()
            print("[Counter] Log file successfully closed")
#    @profile
    def write_count_to_log(self):
        """
        This function will write a row to the log file. The row contains a
        timestamp, number of entries and number of exits.
        """
        if self.log_counting_events:
            if self.csvfile is not None:
                try:
                    self.csvfile.writerow([timee(),
                                        self.get_count_in(),
                                        self.get_count_out()])
                    self.outfile.flush()  # Force flushing after every log line
                except (IOError, OSError) as error:
                    print(error)
#    @profile
    def read_count_in_log(self):
        row_index = 0
        data = []
        if self.restore_counts:
            file_list = glob('logs/*.csv')
            latest_file = max(file_list, key=path.getctime)
            if date.fromtimestamp(path.getctime(latest_file)) == date.today():
                with open(latest_file, "r") as last_log:
                    reader = readerr((x.replace('\0', '') for x in last_log), delimiter=',')
                    for row in reader:
                        if row:
                            row_index += 1
                            columns = [str(row_index), row[0], row[1], row[2]]
                            data.append(columns)
        return data
#    @profile
    def reset_counting(self):
        """
        This function will reset counters and also the tracking class.
        """
        self.counter.reset()

        TrackedObject.reset_id()
        print("[Counter] Counters have been reset")
#    @profile
    def daily_reset(self):
        """
        This function calls functions to be run daily
        """
        self.load_config()
        if self.log_counting_events:
            self.close_log_file()
            self.reset_counting()
            self.init_log_file()
        else:
            self.reset_counting()
#    @profile
    def check_daily_reset(self):
        """
        This function checks if the daily reset needs to be performed and
        schedules the next reset time.
        """
        now = datetime.today()
        if now > self.next_reset and not self.first_reset:
            self.push_data_interval()  # Pushing data just before reset
            print("[Counter] Resetting counter...")
            self.daily_reset()
            print("[Counter] Counter successfully reset")
            self.next_reset = self.next_reset + timedelta(days=1)
        elif self.first_reset:
            if now.time() < self.reset_hour:
                self.next_reset = self.next_reset.replace(
                    hour=self.reset_hour.hour, minute=self.reset_hour.minute,
                    second=0)
            else:
                self.next_reset = self.next_reset.replace(
                    hour=self.reset_hour.hour, minute=self.reset_hour.minute,
                    second=0)
                self.next_reset = self.next_reset + timedelta(days=1)
            self.first_reset = False
#    @profile
    def push_data_interval(self):
        """
        This function checks if data push to the webserver needs to be
        performed
        """
        if self.push_count_to_internet and not self.playback:
            current_time = timee()
            if current_time > self.last_push + self.push_interval:
                # Publish people data every interval
                self.async_push()
                self.last_push = current_time
#    @profile
    def async_push(self):
        """
        This function wraps the asynchronous implementation of the data
        pushing.
        """
        start_new_thread(self.push_data, ())
#    @profile
    def push_data(self):
        """
        This function performs the HTTP requests that pushes data.
        """
        try:
            print("[Counter] Pushing data to server...")
            get(self.push_url.format(self.sensor_id,
                                              self.get_count_in(),
                                              self.get_count_out()),
                         timeout=10.0)
            print("[Counter] Data pushed!")

        except exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except exceptions.RequestException as err:
            print("Requests Exception:", err)
#    @profile
    def image_pre_processing(self, depth_array):        ############# Question about how it works?
        """
        This function applies filters and scaling to a depth array.      
        Params:
            depth_array (array): Depth array to pre-process
        """

        if self.window_size > 1:
            if len(self.__q) == self.window_size:
                self.sum -= self.__q.popleft()
            self.sum += depth_array
            self.__q.append(depth_array)
            self.filtered_array = self.sum / len(self.__q)
        else:
            self.filtered_array = depth_array

        # Normalize to image values
        depth_array_norm = (
                self.filtered_array * self.max_uint8 /
                self.scaling_factor).astype(
            uint8)

#        if self.activate_filter:
#            depth_array_norm[
#                depth_array_norm == 0] = 255 - self.binarize_threshold
#            depth_array_norm = cv2.bilateralFilter(depth_array_norm,
#                                                   self.kernel,
#                                                   self.depth_difference,
#                                                   self.area_checked)

        return depth_array_norm
#    @profile
    def binarize_frame(self, frame):
        """
        This function extracts the foreground by setting to a maximal value
        pixels that are below a defined threshold above the estimated
        background.
        Params:
            frame (array): Depth array to binarize
        Returns:
            Foreground mask as array
        """
        bin_frame = zeros_like(frame)

        exclusion_threshold = int((self.camera_height - self.exclusion_height) * self.max_uint8 / self.scaling_factor)

        bin_frame[where(
            (frame < self.background - self.binarize_threshold) &
            (self.background >= self.binarize_threshold) &
            (frame < exclusion_threshold))] = self.max_uint8
        bin_frame[where(frame == 0)] = 0


########################### APPLICATION PSEUDOCODE OF OPENING


        ## kernel (3,3), iterations=2 if heavy noise
        #bin_frame = morphologyEx(bin_frame, MORPH_OPEN,
        #                             ones((3, 3), uint8),
        #                             iterations=self.iterations_number)


        bin_frame = openingg(bin_frame)

        return bin_frame
#    @profile
    def init_background(self):
        """
        This function gathers all steps required to initialize the background.
        """
        # Here background_intermediate is initialized with the first background
        self.background_intermediate[:] = self.background
#    @profile
    def background_recalculation(self, depth_array):
        #  Compensate factors with update interval
        """
        This function updates the background estimation from a depth image.
        Params:
            depth_array (array): Depth array used to update background
        """
        grow_factor = self.bg_growth_rate * self.bg_frame_interval      ####### units bg_growth_rate
        decay_factor = self.bg_decay_rate * self.bg_frame_interval      ####### "  "  " _decay_rate
        #  Limitation of factor to avoid overflow
        if grow_factor > 1.0:
            grow_factor = 1.0
        if decay_factor > 1.0:
            decay_factor = 1.0

        # In the first step we check if the current depth array is closer to
        # the camera than the background,
        # in that case we add the difference multiplied by the growth rate
        # to the background
        self.background_intermediate = where(
            (depth_array <= self.background_intermediate -
                self.bg_threshold) & (depth_array != 0),
            self.background_intermediate + grow_factor * (
                depth_array - self.background_intermediate),
            self.background_intermediate)
        # In the next step we check if the current depth array is further
        # away from to the camera than the background,
        # in that case we subtract the difference from the background
        self.background_intermediate = where(
            (depth_array >= self.background_intermediate +
                self.bg_threshold) & (depth_array != 255),
            self.background_intermediate + decay_factor * (
                depth_array - self.background_intermediate),
            self.background_intermediate)
        self.background[:] = self.background_intermediate
        self.background.astype(uint8)




#    @profile
    def head_contours_extraction(self, frame, binarized_frame):
        """
        This function is the core of people counting. It is the one that
        extracts heads locations and contours but also distinguishes between
        two people that are close or even touching.
        Params:
            frame (array): Current depth frame
            binarized_frame (array): Foreground mask
        Returns:
            head_contours (list): List of detected contours
            detected * frame (array): Depth frame masked from detected
                contours
            contours_minimas (list): list of each contour minimum
        """
        head_contours = []
        contours_minima = []
        minima_values = []
        detected = zeros(frame.shape, uint8)

        # Compute foreground

##########################################################   APPLICATION OF THE PSEUDOCODE
#        foreground = zeros(frame.shape, uint8)

        closing = closingg(binarized_frame)


        foreground = (closing / self.max_uint8) * frame

#        foreground[:] = (binarized_frame / self.max_uint8) * frame


##        # We change the 0 to 255 because 0 means invalid and not closer
        foreground[foreground == 0] = self.max_uint8

#        foreground = morphologyEx(foreground, MORPH_CLOSE, None,
#                                      iterations=1)


        level = nanmin(where(foreground != 0, foreground, nan))
        max_level = maxx(foreground)


        while (level + self.detect_threshold) < max_level:
            current_slice = zeros(frame.shape, uint8)
            current_slice[foreground < level] = 1.0 ##### potential optimization

            # Find contours
###            if(cv2.__version__[0]!='4'):
###            (_, contours, _) = cv2.findContours(current_slice,
###                                            cv2.RETR_EXTERNAL,
###                                            cv2.CHAIN_APPROX_SIMPLE)
###            else:
            (contours, _) = findContours(current_slice,
                                         RETR_EXTERNAL,
                                         CHAIN_APPROX_SIMPLE)

#            contours = FindContourss(current_slice)

######################################  APPLICATION PSEUDOCODE CONTOUR AREA

            sized_contours = [(cnt, contourAreaa(cnt)) for cnt in contours
                              if contourAreaa(cnt) > self.min_area]



#            sized_contours = [(cnt, contourArea(cnt)) for cnt in contours
#                              if contourArea(cnt) > self.min_area]


            for contour in sized_contours:
#                 Add contour to detected_mask
                contour_mask = zeros(frame.shape, uint8)
#######################################  APPLICATION PSEUDOCODE DRAW CONTOUR
                contourr = squeeze(contour[0], axis=1)
                maxaa=0
                minaa=255
                maxab=0
                minab=255
                for i in range(len(contourr)):
                    if contourr[i][1]>maxaa: maxaa=contourr[i][1]
                    if contourr[i][1]<minaa: minaa=contourr[i][1]
                    if contourr[i][0]>maxab: maxab=contourr[i][0]
                    if contourr[i][0]<minab: minab=contourr[i][0]
                    

                Drawfilledcontour(contour_mask, contour[0], minaa, maxaa, minab, maxab)


#                drawContours(contour_mask, [contour[0]], -1, 1, -1)
                

                extracted_foreground = frame * contour_mask
                extracted_foreground[
                    extracted_foreground == 0] = self.max_uint8




######################################  APPLICATION PSEUDOCODE min location
#                a, b, min_loc, c = minMaxLoc(extracted_foreground)
                a, min_loc = min_contourss(extracted_foreground, minaa, maxaa, minab, maxab)


                if len(sized_contours) > len(contours_minima):
                    if len(head_contours) == 0:
                        contours_minima.append(min_loc)
                        minima_values.append(a)
                        head_contours.append(contour[0])
              #          drawContours(detected, [contour[0]], -1, 1, -1)     # MAYBE REMOVED
                    else:
                        inside_count = 0
                        for old_min in contours_minima:
######################################  APPLICATION PSEUDOCODE POINT POLYGON TEST
#                            dist = pointPolygonTest(contour[0], old_min,
#                                                        False)
                            dist = Polygontestpoint(contour[0], old_min)
                            if dist >= 0:
                                inside_count += 1
                                if inside_count == 1:
                                    index_to_replace = contours_minima.index(
                                        old_min)
                        if inside_count == 0:
                            contours_minima.append(min_loc)
                            minima_values.append(a)
                            head_contours.append(contour[0])
                        else:
                            head_contours[index_to_replace] = contour[0]

#                    drawContours(detected, [contour[0]], -1, 1, -1)     ####### double draw contours?
              #      cx, cy = Polygoncentroid(contour[0]) 
                    Drawfilledcontour(detected, contour[0], minaa, maxaa, minab, maxab)
            level += self.detect_threshold
        return head_contours, detected * frame, contours_minima
#    @profile
    def count_out(self, person):
        """
        This function gathers all steps performed when an OUT event is
        detected.
        Params:
            person (Person): Person that triggered the OUT event
        """
        print("[Counter] ID: {} counted out at {}".format(person.id,
                                                          strftime("%c")))
        if not self.playback:
            self.write_count_to_log()
#    @profile
    def count_in(self, person):
        """
        This function gathers all steps performed when an IN event is detected.
        Params:
            person (Person): Person that triggered the IN event
        """
        print("[Counter] ID: {} counted in at {}".format(person.id,
                                                         strftime("%c")))
        if not self.playback:
            self.write_count_to_log()
#    @profile
    def track_lost_callback(self, person):
        """
        This function is called when the tracking of an object ends.
        Params:
            person (Person): Person that is no longer tracked
        """
        if self.record_on_counting_event:
            if not self.playback:
                self.trigger_record(timee() - person.created_at)
#    @profile
    def trigger_record(self, duration):
        """
        This function gathers steps required to trigger the recording.
        Params:
            duration (int): Duration in sec to be recorded
        """
        self.nb_frame_to_record.value = int(duration * 30)
        self.recording_trigger_event.set()
#    @profile
    def visualization(self, frame, contours, minima):
        """
        This function adds counting information on top of a depth array.
        Params:
            frame (array): Depth frame used for visualization
            contours (list): List of detected contours
            minima (list): List of contours minima
        Returns:
            rgb_frame (array): RGB frame to be displayed
        """
        rgb_frame = cvtColor(frame, COLOR_GRAY2RGB)

        if self.line_edit_mode:
            putText(rgb_frame, "EDIT",
                        (int(0.35 * self.width), int(0.15 * self.height)),
                        self.font, 0.3,
                        (255, 255, 255), 1, LINE_AA)

            # Display counting area
            if len(self.counter.area_polygon) > 0:
                rgb_frame = drawContours(rgb_frame, [self.counter.area_polygon], -1,
                                             self.visualization_colour, 1,
                                             LINE_8)
            return rgb_frame

        # Draws a bounding rectangle for each contour
        for i in range(len(contours)):
            x, y, w, h = boundingRect(contours[i])
            rectangle(rgb_frame, (x, y), (x + w, y + h),
                          self.visualization_colour, 1)

        # Draw the minim of each contour
        for minimum in minima:
            circle(rgb_frame, minimum, 2, (255, 0, 185), -1)

        # Display the tracking ID (white is active and red is untracked) and
        # trajectory
        for person in self.tracker.tracked_objects:
            if person.age == 1:
                c = (255, 255, 255)
            else:
                c = (0, 0, 255)
            putText(rgb_frame, str(person.id), (person.x, person.y),
                        self.font, 0.3, c, 1, LINE_AA)

            for point1, point2 in zip(person.tracks, person.tracks[1:]):
                color = ((person.id * 561) % 255,
                         (person.id * 1105) % 255,
                         (person.id * 1729) % 255)
                linee(rgb_frame, point1, point2, color, 1)

        # Display counting area
        if len(self.counter.area_polygon) > 0:
            rgb_frame = drawContours(rgb_frame, [self.counter.area_polygon], -1,
                                         self.visualization_colour, 1,
                                         LINE_8)

        # Display counts
        str_out = 'OUT: ' + str(self.get_count_out())
        str_in = 'IN: ' + str(self.get_count_in())
        if self.reversed_counting_direction:
            putText(rgb_frame, str_in,
                        (int(0.025 * self.width), int(0.15 * self.height)),
                        self.font, 0.25,
                        self.visualization_colour, 1, LINE_AA)
            putText(rgb_frame, str_out,
                        (int(0.025 * self.width), int(0.95 * self.height)),
                        self.font, 0.25,
                        self.visualization_colour, 1, LINE_AA)
        else:
            putText(rgb_frame, str_out,
                        (int(0.025 * self.width), int(0.15 * self.height)),
                        self.font, 0.25,
                        self.visualization_colour, 1, LINE_AA)
            putText(rgb_frame, str_in,
                        (int(0.025 * self.width), int(0.95 * self.height)),
                        self.font, 0.25,
                        self.visualization_colour, 1, LINE_AA)

        # Display frame per second
        putText(rgb_frame, str(round(self.fps_estimator.get_fps(), 1)),
                    (int(0.70 * self.width), int(0.15 * self.height)),
                    self.font, 0.25,
                    self.visualization_colour, 1, LINE_AA)

        return rgb_frame

#################################################################################################################################################
#    @profile
    def get_frame(self, timeout):
        """
        This function waits for a ready frame from the shared array use
        between this object and the frame producer. If a timeout occurs,
        it will return None. This function will synchronize the counter to
        the rate of the frame producer.
        Params:
            timeout (int): Time in sec before aborting the wait
        Returns:
            depth_array (array): Depth frame received from frame producer
        """
        # Wait for the device to be ready
        if (not self.pause or self.get_once) and \
                self.device_ready.wait(timeout):

            # Create numpy array on top of shared memory buffer, then we
            # make a copy to freeze the frame
            array_from_buffer = frombuffer(self.shared_array.get_obj(),
                                              dtype='I').reshape(
                self.shared_array_dim)
            depth_array = copy(array_from_buffer)

            # We signal the driver that the frame has been taken and a new
            # one can be written to the buffer
            self.device_ready.clear()
            self.get_once = False
            return depth_array
        else:
            return None
#    @profile
    def wait_for_key(self):
        """
        This function handles the OpenCV I/O loop which is based on the
        waitKey() function. This is also where key press behaviour is defined.
        """
        any_window = self.display_background or self.display_binarized or \
                     self.display_detected or self.display_visualization

        if any_window:
            # Waiting for key
            key = waitKey(1)
            if key & 0xEFFFFF == 27:  # "ESC"
                raise KeyboardInterrupt()
            elif key & 0xEFFFFF == 114:  # "r"
                self.reset_counting()
            elif key & 0xEFFFFF == 32:  # "space"
                if self.pause:
                    self.pause = False
                    print("[Counter] Resumed")
                else:
                    self.pause = True
                    print("[Counter] Paused")
            elif key & 0xEFFFFF == 83:  # "right-arrow"
                if self.pause:
                    self.get_once = True
                    print("[Counter] Next frame")
            elif key & 0xEFFFFF == 81:  # "left-arrow"
                pass
            elif key & 0xEFFFFF == 105:
                self.counter.count_in += 1
            elif key & 0xEFFFFF == 111:
                self.counter.count_out += 1
            elif key & 0xEFFFFF == 101:
                if self.line_edit_mode:
                    self.line_edit_mode = False
                    try:
                        if len(self.counter.area_polygon.tolist()) > 0:
                            self.cfg.yaml_dict["counting_params_user"][
                                "in_area"] = self.counter.area_polygon.tolist()
                            self.cfg.save_config()
                    except Exception as e:
                        print(e)
                    setMouseCallback(WinName.VIS, lambda *args : None)
                else:
                    self.line_edit_mode = True
                    self.first_click = True
                    setMouseCallback(WinName.VIS, self.on_mouse_event)
##    @profile
    def on_mouse_event(self, event, x, y, flags, *params):
        """
        Function that processes mouse events
        Params:
            event (int): type of mouse event
            x (int): x position of cursor
            y (int): y position of cursor
            flags (int): additionnal flags such as other button/key pressed

        """
        if event == EVENT_LBUTTONUP:
            if flags & EVENT_FLAG_CTRLKEY:
                if self.first_click:
                    self.first_click = False
                new_line = self.counter.area_polygon.tolist()
                if len(new_line) > 0:
                    new_line.pop()
                self.counter.area_polygon = array(new_line)
            else:
                if self.first_click:
                    self.counter.area_polygon = array([])
                    self.first_click = False
                new_line = self.counter.area_polygon.tolist()
                new_line.append([x, y])
                self.counter.area_polygon = array(new_line)
#    @profile
    def run(self):
        """
        This function is the main loop of the people counting software. It
        contains the pipeline definition along to calls to all necessary
        functions.
        """
#        h = hpy()
        self.n_frame = -1
        n_frame = -1
        try:
            while True:
                depth_array = self.get_frame(0.1)
                if depth_array is not None:
                    n_frame += 1
                    self.n_frame += 1
                else:
                    self.wait_for_key()
                    continue

                if n_frame == 0:                                             ##### THIS IS THE FIRST THING DONE
                    # The first frame we receive is the estimated background
                    # done by the driver at start
                    self.background = self.image_pre_processing(depth_array)
                    self.init_background()
                    if self.auto_compute_params and not self.playback:
                        self.binarize_threshold = self.shared_variables[
                            "binarized_threshold"].value
                        self.detect_threshold = self.shared_variables[
                            "detect_threshold"].value
                        self.min_area = self.shared_variables["min_area"].value
                    continue
                elif n_frame == 1:
                    if self.middle_pixel_check:
                        mid_pxl = self.driver.middle_pixel_depth(depth_array)
                        if mid_pxl == 0:
                            self.driver.shutdown()
                            print("[Counter] Inconsistent central pixel " \
                                  "value, shutting down program...")
                            exit()
                            return False

                # Detection workflow
                preprocessed_frame = self.image_pre_processing(depth_array)
                binarized_frame = self.binarize_frame(preprocessed_frame)
                motion_contours, detection_mask, minima = \
                    self.head_contours_extraction(
                        preprocessed_frame, binarized_frame)
                self.tracker.track_contours(motion_contours)
                self.counter.update_count_multi(self.tracker.tracked_objects)

                # Add visualization infos on frame
                visualization_frame = self.visualization(preprocessed_frame,
                                                         motion_contours,
                                                         minima)

                if self.bg_frame_interval > 0:
                    if n_frame % self.bg_frame_interval == 0 and n_frame != 0:
                        # Every bg_frame_interval the background is updated
                        self.background_recalculation(preprocessed_frame)

                if self.display_visualization:
                    namedWindow(WinName.VIS, WINDOW_NORMAL)
                    if n_frame == 1:
                        moveWindow(WinName.VIS, 0, 0)
                    imshow(WinName.VIS, visualization_frame)
                if self.display_background:
                    namedWindow(WinName.BGD, WINDOW_NORMAL)
                    if n_frame == 1:
                        moveWindow(WinName.BGD, 0, 500)
                    imshow(WinName.BGD, self.background)
                if self.display_binarized:
                    namedWindow(WinName.BIN, WINDOW_NORMAL)
                    if n_frame == 1:
                        moveWindow(WinName.BIN, 500, 0)
                    imshow(WinName.BIN, binarized_frame)
                if self.display_detected:
                    namedWindow(WinName.DET, WINDOW_NORMAL)
                    if n_frame == 1:
                        moveWindow(WinName.DET, 500, 500)
                    imshow(WinName.DET, detection_mask)


                self.fps_estimator.tick()

                # Check for day change to reset counting
                self.check_daily_reset()
                self.push_data_interval()

                self.wait_for_key()

        except IndexError:
            print(self.get_count_in(), self.get_count_out())
            destroyAllWindows()
            raise

        except KeyboardInterrupt:
            self.close_log_file()
            self.stop.value = True
            destroyAllWindows()
            print("[Counter] Closing from keyboard interrupt")
#        print(h.heap())

    @staticmethod
    def instantiate_counter_from_args(arg_list):
        """
        This method will parse and check arguments.
        Params:
            arg_list (list): List of arguments comming from the command line
        Returns:
            A MultiplePeopleCounter object or False is there is an error
        """
        args = arg_list
        argc = len(args)

        if argc == 1:
            print("[Counter] Starting people counting live from camera")
            return MultiplePeopleCounter()
        elif argc == 2:
            print("[Counter] Reading from file: {}".format(args[1]))
            return MultiplePeopleCounter(args[1])
        elif argc == 3:
            try:
                if not float(args[2]) > 0:
                    print("Incorrect rate range")
                    return False

            except ValueError:
                print("Specified rate is not a number")
                return False

            print("[Counter] Reading from file: {}".format(args[1]))
            return MultiplePeopleCounter(args[1], args[2])
        else:
            print("[Counter] Invalid number of arguments")
            return False


