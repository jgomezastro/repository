# -*- coding: utf-8 -*-
from numpy import zeros
from numpy import roll


class RingBuffer(object):
    """
    This class is the implementation of a simple ring buffer used to buffer
    2D frames.
    """
    def __init__(self, h, w, length):
        """
        This function initializes the data structure that is going to hold
        the buffer.
        Params:
            h (int): First dimension of the buffer, here height is assumed
            w (int): Second dimension of the buffer, here widtht is assumed
            lentgh (int): Third dimension of the buffer, this is the one
                going to be rolled on
        """
        self.data = zeros((h, w, length), dtype='uint16')

    def extend(self, x):
        """
        This function adds the x element to the end of the buffer and removes
        the oldest/first element.
        Params:
            x (np.Array): Element to be added to the buffer
        """
        self.data = roll(self.data, -1, axis=2)
        self.data[:, :, -1] = x
