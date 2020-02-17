# -*- coding: utf-8 -*-
from time import time


class TrackedObject(object):
    """
    This class is the base class for any object that needs to be tracked by
    trackers available in Trackers.py.
    """
    id_index = 0

    @classmethod
    def get_next_id(cls):
        """This function returns a growing id used by any daughter class."""
        next_id = cls.id_index
        cls.id_index += 1
        return next_id

    @classmethod
    def reset_id(cls):
        """This function resets the id generation."""
        cls.id_index = 0

    def __init__(self, x, y):
        """
        This function creates a TrackedObject with x and y as starting
        coordinates.
        Params:
            x (int)
            y (int)
        """
        self.id = TrackedObject.get_next_id()
        self.age = 0

        self.x = x
        self.y = y
        self.tracks = []

        self.created_at = time()

    def update_location(self, xn, yn):
        """
        This function updates coordinates of the TrackedObjectwith xn and yn as
        new coordinates.
        Params:
            xn (int)
            yn (int)
        """
        self.age = 0
        self.tracks.insert(0, (xn, yn))
        if len(self.tracks) > 1800:  # Prevent unlimited trajectory length
            self.tracks.pop()
        self.x = xn
        self.y = yn

    def age_one(self):
        """
        This function increments the age attribute.
        """
        self.age += 1

    def get_loc(self):
        """
        Returns the location of the tracked object
        """
        return self.x, self.y


class Person(TrackedObject):
    """
    This class inherits from TrackedObject and is used to track a Person
    position and features.
    """
    def __init__(self, x, y):
        super(Person, self).__init__(x, y)

        self.last_direction = None
        self.height = 0

    def update_location(self, xn, yn):
        """
        This function updates a TrackedObject with xn and yn as new
        coordinates.
        Params:
            xn (int)
            yn (int)
        """
        super(Person, self).update_location(xn, yn)
