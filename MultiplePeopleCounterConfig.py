# -*- coding: utf-8 -*-
import functools

from ruamel.yaml import YAML              ###### untouchable ???
yaml = YAML()


class ConfigSection(object):
    """
    This class is the base element of a recursive structure used to
    represent a config file as an object for dot-access of attributes.
    """

    def __init__(self, **kwords):
        self.__dict__.update(kwords)

    def rsetattr(self, attr, val):
        """Recursively sets attribute."""
        pre, _, post = attr.rpartition('.')
        return setattr(self.rgetattr(self, pre) if pre else self, post, val)

    def rgetattr(self, attr, *args):
        """Recursively gets attribute."""

        def _getattr(obj, attr):
            try:
                return getattr(obj, attr, *args)
            except AttributeError:
                return None

        return functools.reduce(_getattr, [self] + attr.split('.'))


def print_config_from_dict(cfg_dict, depth=0):
    """
    This function recursively prints a yaml loaded as dict.
    Params:
        cfg_dict (dict): Dict of a loaded YAML
        depth (int): Recursive depth parameter
    """
    # Pretty print yaml config recusively
    for elem in cfg_dict:
        if isinstance(cfg_dict[elem], dict):
            print("[Counter] " + '  ' * depth + "[{}]".format(elem))
            print_config_from_dict(cfg_dict[elem], depth + 1)
        else:
            print("[Counter] " + '  ' * depth + "{} = {}".format(
                elem, cfg_dict[elem]))


class MultiplePeopleCounterConfig(ConfigSection):
    """
    This class is based on the ConfigSection class. It goals is to recursively
    load a YAML file in an object to allow dot-access.
    """

    def __init__(self, filename):
        ConfigSection.__init__(self)
        self.filename = filename
        self.yaml_dict = {}

        self.read_config_file()

    def create_sections(self, cfg_dict, depth=0):
        """
        This function recursively instantiates ConfigSection for each
        sections in the YAML file.
        """
        if depth == 0:  # Set attributes of current class if at first yaml
            # level
            for elem in cfg_dict:
                setattr(self, elem, cfg_dict[elem])  # Initial set of settings

                # Now if there is a nested dict (i.e. sub-section),
                # we replace it by a ConfigSection object (for direct dot
                # access) recursively
                if isinstance(cfg_dict[elem], dict):
                    setattr(self, elem,
                            self.create_sections(cfg_dict[elem], depth + 1))

        # If we are not a first level we create ConfigSection objects from
        # dict and return them to upper level
        elif depth > 0:
            section = ConfigSection(
                **cfg_dict)  # Initial ConfigSection instantiation

            # Now if there is a nested dict, we replace it by a
            # ConfigSection by recursive call to current function
            for elem in cfg_dict:
                if isinstance(cfg_dict[elem], dict):
                    setattr(section, elem,
                            self.create_sections(cfg_dict[elem], depth + 1))
            return section

    def read_config_file(self):
        """
        This function prints and loads a YAML file into a
        MultiplePeopleCounterConfig object.
        """
        try:
            with open(self.filename, 'r') as ymlfile:
                self.yaml_dict = yaml.load(ymlfile)
                print_config_from_dict(self.yaml_dict)
                self.create_sections(self.yaml_dict)

        except (IOError, OSError) as error:
            print(error)
            print("[Counter] Config file {} not found. " \
                  "Using default parameters".format(self.filename))

    def save_config(self):
        """
        This function write the "yaml_dict" variable to the file named in
        the "filename" variable
        """
        try:
            with open(self.filename, 'w') as ymlfile:
                yaml.dump(self.yaml_dict, ymlfile)

        except (IOError, OSError) as error:
            print(error)
            print("[Counter] Error when writing config file {}" \
                  .format(self.filename))
