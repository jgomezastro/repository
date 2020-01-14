# -*- coding: utf-8 -*-
from sys import argv

import MultiplePeopleCounter as MPC

#from memory_profiler import profile      ########################## linea introducida por mi

#@profile      ########################## linea introducida por mi
def display_usage():
    """
    This function displays the command line usage.
    """
    print("Usage: python2 people_counting_depth.py [<filename> [<replay " \
          "rate>]]")
    print(" - If filename is not specified the script will try to connect to "\
          "a depth camera")
    print(" - If replay rate is not specified the default value is 30 fps")

#@profile      ########################## linea introducida por mi
def display_version():
    """
    This function displays the version defined in MultiplePeopleCounter.py.
    """
    verline = "# Terabee Multiple Counting v{} #".format(MPC.__version__)
    print("#" * len(verline))
    print(verline)
    print("#" * len(verline))

#@profile      ########################## linea introducida por mi
def main():
    """
    This function is a wrapper, its role is to instantiate and run the main
    class.
    """

    display_version()
    counter = MPC.MultiplePeopleCounter.instantiate_counter_from_args(argv)

    if not counter:
        display_usage()
        exit()
    else:
        try:
            counter.run()
        except Exception:
            counter.close_log_file()


if __name__ == "__main__":
    main()
