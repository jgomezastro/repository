# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext

ext_modules = [
    Extension("RingBuffer", ["RingBuffer.py"]),
    Extension("DriverProcess", ["DriverProcess.py"]),
    Extension("FileReaderProcess", ["FileReaderProcess.py"]),
    Extension("Terabee3DcamDriver", ["Terabee3DcamDriver.py"]),
    Extension("MultiplePeopleCounter", ["MultiplePeopleCounter.py"]),
    Extension("MultiplePeopleCounterConfig", ["MultiplePeopleCounterConfig.py"]),
    Extension("Person", ["Person.py"]),
    Extension("people_counting_depth_cam", ["people_counting_depth_cam.py"]),
    Extension("FpsEstimator", ["FpsEstimator.py"]),
    Extension("Trackers", ["Trackers.py"]),
    Extension("Detectors", ["Detectors.py"]),
    Extension("Counters", ["Counters.py"]),
]

setup(
    name='MPC',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
