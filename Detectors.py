# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod

class DetectorType(object):
    """
    This class enumerates the different types of Detectors.
    """
    SLICE_MIN = 0
    WATER_FILLING = 1


class AbstractDetector(object):
    """
    This abstract class is the base for any detector class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, min_area):
        self.min_area = min_area

    @abstractmethod
    def detect(self, frame, foreground_mask):
        """
        This function is the main function of the Detector class. It
        needs to be implemented by daughter classes.
        Params:
            frame (np.Array): Depth image where detection needs to be performed
            foreground_mask (np.Array): 0 when background and 1 when foreground
        """
        pass


class SliceMinDetector(AbstractDetector):
    def __init__(self, min_area):
        super(SliceMinDetector, self).__init__(min_area)

    def detect(self, frame, foregrund_mask):
        pass


class WaterFillingDetector(AbstractDetector):

    def __init__(self, min_area):
        super(WaterFillingDetector, self).__init__(min_area)

    def detect(self, frame, foregrund_mask):
        pass
