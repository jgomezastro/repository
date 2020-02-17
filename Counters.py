# coding=utf-8
from abc import abstractmethod          ###### untouchable ???
#from cv2 import pointPolygonTest          ###### untouchable ???
from Polygontestpointt import Polygontestpoint

class CounterType(object):
    """
    This class enumerates the different Counter types.
    """
    LINE = 0
    AREA = 1


class AbstractInOutCounter(object):
    """
    This class is the base class for any counting class.
    """
    def __init__(self, reversed_counting_logic):
        self.count_in = 0
        self.count_out = 0

        # Lists of functions to call on in/out events
        self.out_event_callbacks = []
        self.in_event_callbacks = []

        self.reversed_counting = reversed_counting_logic
        self.counts = {}

    def register_out_event_callback(self, callback_function):
        """
        This function registers a function to be triggered by out events
        Params:
            callback_function (function)
        """
        self.out_event_callbacks.append(callback_function)

    def register_in_events_callback(self, callback_function):
        """
        This function registers a function to be triggered by in events
        Params:
            callback_function (function)
        """
        self.in_event_callbacks.append(callback_function)

    def reset(self):
        """
        This function resets counters to zero
        """
        self.count_in = 0
        self.count_out = 0

    @abstractmethod
    def update_count(self, tracked_object):
        """
        This function updates counts when a TrackedObject is updated,
        It needs to be implemented by daughter classes.
        Params:
            tracked_object (TrackedObject): object that has been updated
        """
        pass

    def update_count_multi(self, tracked_objects):
        """
        This function allows updating counts of multiple objects by
        passing a list of tracked objects.
        Params:
            tracked_objects (list): list of tracked objects to update the
            counting of
        """
        for tracked_object in tracked_objects:
            self.update_count(tracked_object)

    @abstractmethod
    def get_final_count(self, tracked_object):
        """
        This function computes the final direction of an object and notifies
        the corresponding event to listeners. It also deletes the
        corresponding key in the "counts" dictionnary.
        """
        pass

    def notify_out_event(self, tracked_object):
        """
        This function calls all functions that should be triggered by out
        events
        Params:
            tracked_object (TrackedObject): object that triggered the event
        """
        self.count_out += 1
        for callback in self.out_event_callbacks:
            callback(tracked_object)

    def notify_in_event(self, tracked_object):
        """
        This function calls all functions that should be triggered by in events
        Params:
            tracked_object (TrackedObject): object that triggered the event
        """
        self.count_in += 1
        for callback in self.in_event_callbacks:
            callback(tracked_object)


class AreaCounter(AbstractInOutCounter):
    """
    This class derives the AbstractInOutCounter. It implements a counting
    method based on the crossing the border of an area.
    """
    def __init__(self, area_points, reversed_counting_logic):
        """
        Initializes the area counter object
        Params:
            area_points (List): list of points that define the counting area
        """
        super(AreaCounter, self).__init__(reversed_counting_logic)
        if len(area_points) > 2:
            self.area_polygon = area_points
        else:
            print("[Counter] Invalid counting area settings, the counter" \
                  " will use the bottom half of the image by default")
            self.area_polygon = [[0, 30], [79, 30], [79, 59], [0, 59]]

    def update_count(self, tracked_object):
        """
        This function tests if an object crossed the border of the
        counting area. It also checks in which direction.
        Params:
            tracke_object (TrackedObject): object to check
        """
        if len(self.area_polygon) < 3:
            return
######################################  APPLICATION PSEUDOCODE POINT POLYGON TEST

#        res = pointPolygonTest(self.area_polygon, tracked_object.get_loc(),
#                                   measureDist=False)     ######### The function determines whether the point is inside a contour, outside, or lies on an edge (or coincides with a vertex). It returns positive (inside), negative (outside), or zero (on an edge) value, correspondingly. When measureDist=false , the return value is +1, -1, and 0, respectively. Otherwise, the return value is a signed distance between the point and the nearest contour edge.
        res = Polygontestpoint(self.area_polygon, tracked_object.get_loc())

        # Add the object to the count list if first time
        if tracked_object not in self.counts:
            self.counts[tracked_object] = {"nb_up": 0, "nb_down": 0,
                                           "last_test_result": res}

        if res >= 0:
            if self.counts[tracked_object]["last_test_result"] < 0:
                self.counts[tracked_object]["nb_up"] += 1
        elif res < 0:
            if self.counts[tracked_object]["last_test_result"] >= 0:
                self.counts[tracked_object]["nb_down"] += 1

        self.counts[tracked_object]["last_test_result"] = res

    def get_final_count(self, tracked_object):
        """
        This function computes the final direction of an object and notifies
        the coressponding event to listeners. It also deletes the
        corresponding key in the "counts" dictionnary.
        """
        if tracked_object in self.counts:
            nb_up = self.counts[tracked_object]["nb_up"]
            nb_down = self.counts[tracked_object]["nb_down"]
            if not self.reversed_counting:
                if nb_up < nb_down:
                    self.notify_out_event(tracked_object)
                elif nb_up > nb_down:
                    self.notify_in_event(tracked_object)
            else:
                if nb_up < nb_down:
                    self.notify_in_event(tracked_object)
                elif nb_up > nb_down:
                    self.notify_out_event(tracked_object)

            self.counts.pop(tracked_object, None)
