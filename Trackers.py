# -*- coding: utf-8 -*-
from abc import ABCMeta          ###### untouchable ???
from abc import abstractmethod          ###### untouchable ???

from cv2 import moments          ###### untouchable ???
from cv2 import boundingRect

from Person import Person            ###### untouchable ???


class TrackerType(object):
    """
    This class enumerates the different Tracker types.
    """
    GREEDY = 0
    PROXIMITY = 1


class AbstractTracker(object):
    """
    This abstract class is the base for any tracker class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, max_age):
        """
        Params
            max_age (int): Maximum number of times a tracked object is allowed
                to not be updated. Any tracked object older than this will
                stop being tracked
            on_track_lost_callback (function): Function called when a track
                is lost
            on_update_callback (function): Function called when a tracked
                object is updated
        """
        self.tracked_objects = []
        self.max_age = max_age
        self.on_track_lost_callbacks = []
        self.on_object_updated_callbacks = []

    def register_on_track_lost_callback(self, callback_function):
        """
        This function registers a function to be triggered by track lost events
        Params:
            callback_function (function)
        """
        self.on_track_lost_callbacks.append(callback_function)

    def register_on_object_updated_callback(self, callback_function):
        """
        This function registers a function to be triggered by object updated
        events
        Params:
            callback_function (function)
        """
        self.on_object_updated_callbacks.append(callback_function)

    def notify_on_track_lost_event(self, tracked_object):
        """
        This function calls all functions that should be triggered by
        on_track_lost events
        Params:
            tracked_object (TrackedObject): object that triggered the event
        """
        for callback in self.on_track_lost_callbacks:
            callback(tracked_object)

    def notify_on_object_updated_event(self, tracked_object):
        """
        This function calls all functions that should be triggered by
        on_object_updated events
        Params:
            tracked_object (TrackedObject): object that triggered the event
        """
        for callback in self.on_object_updated_callbacks:
            callback(tracked_object)

    @abstractmethod
    def track_contours(self, contours):
        """
        This function is the main tracking function of the Tracking class. It
        needs to be implemented by daughter classes.
        Params:
            contours (list): List of contours to track
        """
        pass

    def maintain_tracking_list(self):
        """
        This function is called regularly to performs actions on the active
        tracking list. For instance, this is where old elements are removed.
        """
        for elem in self.tracked_objects:
            if elem.age > self.max_age:
                if len(self.on_track_lost_callbacks) > 0:
                    self.notify_on_track_lost_event(elem)
                else:
                    print("[Tracker] Lost track of {}".format(elem))

                index = self.tracked_objects.index(elem)
                self.tracked_objects.pop(index)
                del elem
            else:
                elem.age_one()


class GreedyTracker(AbstractTracker):
    """
    This tracker implements a greedy algorithm to match a contour to a
    tracked person. In the Greedy implementation a contour is assigned to
    the first person that is within the bounding rectangle of a contour. A
    matching_ratio parameter is applied on the dimensions of the bounding
    rectangle to allow matching outside or only inside of the bounding
    rectangle.

    """
    def __init__(self, max_age, track_lost_callback, matching_ratio=1.3):
        super(GreedyTracker, self).__init__(max_age)
        self.register_on_track_lost_callback(track_lost_callback)
        self.matching_ratio = matching_ratio

    def track_contours(self, contours):
        """
        This function is the main tracking function.
        Params:
            contours (list): List of contours to track
        """
        contour_assigned = [False] * len(contours)

        for i in range(len(contours)):
            # Image moments help you to calculate some features like center
            # of mass of the object, area of the object
            contour_moment = moments(contours[i])
            # From this moments, you can extract useful data like area,
            # centroid etc.
            # Centroid is given by the relations, Cx=M10/M00 and Cy=M01/M00.
            # This can be done as follow:
            cx = int(contour_moment['m10'] / contour_moment['m00'])
            cy = int(contour_moment['m01'] / contour_moment['m00'])
            # It is a straight rectangle, it doesn't consider the rotation
            # of the object.
            # So area of the bounding rectangle won't be minimum
            x, y, w, h = boundingRect(contours[i])

            contour_not_matched = True
            for person in self.tracked_objects:
                if (abs(cx - person.x) <= (w / 2.0) * self.matching_ratio and
                        abs(cy - person.y) <= (h / 2.0) * self.matching_ratio):
                    if not contour_assigned[i]:
                        contour_not_matched = False
                        contour_assigned[i] = True
                        person.update_location(cx, cy)

            if contour_not_matched:
                new_person = Person(cx, cy)  # , self.line_up, self.line_down)
                self.tracked_objects.append(new_person)

        self.maintain_tracking_list()


class ProximityTracker(AbstractTracker):
    """
    This tracker implements a matching algorithm based on the contour-person
    distance. In this implmentation called Proximity, every person-contour
    assignment is tested. The algorithm prioritize assignments that minimize
    the person-contour distance. The max_tracking_distance is the maximum
    distance allowed for an assignment, beyond this distance a new tracked
    object will be created.
    """
    def __init__(self, max_age, track_lost_callback, max_tracking_distance=12):
        super(ProximityTracker, self).__init__(max_age)
        self.register_on_track_lost_callback(track_lost_callback)
        self.max_tracking_distance = max_tracking_distance**2

    def track_contours(self, contours):
        """
        This function is the main tracking function.
        Params:
            contours (list): List of contours to track
        """
        contour_not_assigned = []
        contour_not_assigned[:] = contours
        partnerships = []

        for i in range(len(contours)):
            # Image moments help you to calculate some features like center
            # of mass of the object, area of the object
            contour_moment = moments(contours[i])
            # From this moments, you can extract useful data like area,
            # centroid etc.
            # Centroid is given by the relations, Cx=M10/M00 and Cy=M01/M00.
            # This can be done as follow:
            cx = int(contour_moment['m10'] / contour_moment['m00'])
            cy = int(contour_moment['m01'] / contour_moment['m00'])

            # Here we create the list of possible contour-person
            # associations called partnership
            # along with the respective distance
            for person in self.tracked_objects:
                euclidean_dist = (cx - person.x) ** 2 + (cy - person.y) ** 2
                if euclidean_dist < self.max_tracking_distance:
                    partnerships.append(
                        {"dist": euclidean_dist, "person": person,
                         "contour": contours[i], "cx": cx, "cy": cy})

            # We sort partnerships by increasing person id so in case of
            # distance equality
            # who was tracked first is assigned first
            partnerships.sort(key=lambda p: p["person"].id)

        # This loop runs until there is no partnership left ################### AQUIIIIII ME QUEDEEEEEEEEEEEEE ###########################################################
        while len(partnerships) > 0:
            best_partnerships = []

            # This parts looks for the best partnership (smallest distance)
            # for a person
            for person in self.tracked_objects:
                best_partnership = {}
                min_dist = float('inf')

                for partnership in partnerships:
                    if partnership["person"] is person:
                        if partnership["dist"] < min_dist:
                            min_dist = partnership["dist"]
                            best_partnership = partnership
                if best_partnership:
                    best_partnerships.append(best_partnership)

            # Now for each contour we check how many times it is the closest
            # to a previously tracked person
            for contour in contours:
                contour_bests = []
                for partnership in best_partnerships:
                    if partnership["contour"] is contour:
                        contour_bests.append(partnership)

                # Case where a contour is not the closest for anyone
                if len(contour_bests) == 0:
                    pass
                # Case where a contour is the closest only for one people
                elif len(contour_bests) == 1:
                    # We assign the contour location to the tracked person
                    cx = contour_bests[0]["cx"]
                    cy = contour_bests[0]["cy"]
                    contour_bests[0]["person"].update_location(cx, cy)

                    # Then we remove any partnership that includes this contour
                    id_to_remove = id(contour_bests[0]["contour"])
                    for index in range(len(contour_not_assigned)):
                        if id(contour_not_assigned[index]) == id_to_remove:
                            contour_not_assigned.pop(index)
                            break

                    # Then we remove any partnership that includes this person
                    indexes_to_remove = []
                    for partnership in partnerships:
                        same_person = partnership["person"] is \
                                      contour_bests[0]["person"]
                        same_contour = partnership["contour"] is \
                                      contour_bests[0]["contour"]

                        # We remove every partnership that has the same
                        # contour or the same person
                        if same_person or same_contour:
                            indexes_to_remove.append(
                                partnerships.index(partnership))

                    indexes_to_remove.sort(reverse=True)
                    # We remove the final partnership
                    for index in indexes_to_remove:
                        partnerships.pop(index)

                # Case where a contour is the closest for more than one people
                elif len(contour_bests) > 1:
                    optimal = contour_bests[0]
                    # We look for the smallest dist among the bests
                    for partnership in contour_bests:
                        if partnership["dist"] < optimal["dist"]:
                            optimal = partnership

                    # We assign the contour location to the tracked person
                    cx = optimal["cx"]
                    cy = optimal["cy"]
                    optimal["person"].update_location(cx, cy)

                    # Then we remove any partnership that includes this contour
                    id_to_remove = id(optimal["contour"])
                    for index in range(len(contour_not_assigned)):
                        if id(contour_not_assigned[index]) == id_to_remove:
                            contour_not_assigned.pop(index)
                            break

                    # Then we remove any partnership that includes this person
                    indexes_to_remove = []
                    for partnership in partnerships:
                        same_person = partnership["person"] is optimal[
                            "person"]
                        same_contour = partnership["contour"] is optimal[
                            "contour"]

                        # We remove every partnership that has the same
                        # contour or the same person
                        if same_person or same_contour:
                            indexes_to_remove.append(
                                partnerships.index(partnership))

                    indexes_to_remove.sort(reverse=True)
                    # We remove the final partnership
                    for index in indexes_to_remove:
                        partnerships.pop(index)

        # Then if there are contours that are not assigned we create a new
        # tracked person
        if len(contour_not_assigned) > 0:
            for cnt in contour_not_assigned:
                contour_moment = moments(cnt)
                cx = int(contour_moment['m10'] / contour_moment['m00'])
                cy = int(contour_moment['m01'] / contour_moment['m00'])
                self.tracked_objects.append(
                    Person(cx, cy))

        self.maintain_tracking_list()
