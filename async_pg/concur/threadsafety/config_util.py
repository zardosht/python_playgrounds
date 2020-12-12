#!/usr/bin/env python
# -*- coding: utf-8 -*-


import yaml
from types import SimpleNamespace


class Config(SimpleNamespace):
    """
    Allows using dot notation for accessing values of a nested
    dictionary. You can access the underlying dictionary of each 
    config level using `as_dict()` method.

    Create a nested namespace from a nested config dictionary.
    Source: https://stackoverflow.com/a/54332748/228965
    """
    def __init__(self, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__setattr__(key, Config(**value))
            else:
                self.__setattr__(key, value)

    def as_dict(self):
        """Return a dictionary of config key-value pairs.

        Return a dictionary of config key-value pairs. If you use 
        nested namespace (dot notation) for configs, it returns the
        underlying dictionary of the current config object (the one
        you called `as_dict()` on).

        :return: A dictionary of config key-value pairs. 
        :rtype: dict
        """
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
                d.setdefault(key, value.as_dict())
            d.setdefault(key, value)

        return d


_config = None


def load_config(conf_file_path: str) -> Config:
    """
    Load the config and returns a config namespace.

    Args
    :params conf_file_path: path to the config file

    Returns
    :return: an instance of Config class with configuration 
        parameters
    """
    global _config
    with open(conf_file_path) as conf_file:
        config_dict = yaml.load(conf_file, yaml.SafeLoader)
        _config = Config(**config_dict)
        return _config


def get_config(conf_file_path:str=None) -> Config:
    """
    If the config is loaded, ruturns it. 
    Otherwise tries to load the config from the given path.
    If no path is given and config is not loaded, raises exception. 

    :param conf_file_path: path to the config.yml file, defaults to None
    :type conf_file_path: str, optional
    :raises ValueError: If config is not loaded and no path is given to load it.
    :return: an instance of the config nested namespace
    :rtype: Config
    """    
    global _config
    if _config is None:
        if conf_file_path is None:
            raise ValueError("No path given for the config file.")

        _config = load_config(conf_file_path)

    return _config


def get(key:str):
    if _config is None:
        raise RuntimeError("Config is not loaded yet. " 
                           "Call load_config(path) first.")
   
    return _config.as_dict()[key]

