"""Utilities module

Contains helper functions and file saving/loading functions.
"""
from __future__ import annotations

import logging
import os
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
from importlib import import_module
from pathlib import Path

imported_functions = {}


LOGGER = logging.getLogger(__name__)


def random_seed():
    """Generate random integer using operating system urandom.

    :return: random integer to use as seed
    """
    return int.from_bytes(os.urandom(8), byteorder="big")


class Configuration:
    """This class is used to hold a configuration in both a dictionary form and
    a hierarchical objet style.

    It's is generic, and can override any attribute/method of another object,
    provided the object's class inherits from this class, by calling
    :meth:`configure`.

    Methods are overriden by providing at the same hierarchical level the
    following keys:

    * "function": the name of the function as it will be imported
    * "args": any passable ordered arguments as a list
    * `*`: any keyworded argument can be provided using its keyword

    :class:`ImportedFunction` objects are used to hold the overriden methods.

    :param dico: configuration in a dictionary form (potentially nested)

    .. warning::
        Avoid using class composition and inheriting from this class, as
        the :meth:`configure` call will replace any nested structure by a
        :class:`Configuration` object. Top-level class however is already
        kept in place.

    .. todo::
        Find a way to replace this class structure by another method which
        keeps the class composition on :meth:`configure` calls. Perhaps using
        a metaclass?
    """

    def __init__(self, dico=None):
        dico = {} if dico is None else dico
        self._config = dico
        for k, v in dico.items():
            if type(v) == dict:
                setattr(self, k, self.configure(v))
            else:
                setattr(self, k, v)

    def __iter__(self):
        for k, v in self._config.items():
            yield k, v

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        self._config[key] = value
        if type(value) is dict:
            setattr(self, key, self.configure(value))
            return
        setattr(self, key, value)

    @classmethod
    def configure(cls, dico):
        """Create an object using the provided configuration.

        :param dico: configuration
        :type dico: dict
        :return: configured object
        :rtype: Configuration
        """
        if "function" in dico:
            return ImportedFunction(dico)
        return Configuration(dico)


class ProcessConfiguration(Configuration):
    """This class defines a configured object with only functions on one level.

    It is used to call a sequence of configurable functions (such as seeds).
    """

    def call_all_functions(self):
        """Call all the functions located in the top-level section"""
        for k in dict(self).keys():
            attr = getattr(self, k)
            if callable(attr):
                attr()


class ImportedFunction(Configuration):
    """This class defines a configurable imported function.

    :param function:
        either the function name or its whole configuration as a dictionary
    :param args: all default ordered arguments
    :param kwargs: all default keyword arguments
    """

    def __init__(self, function, *args, **kwargs):
        if type(function) == dict:
            config = function
        else:
            config = {"function": function}
            if len(args) > 0:
                config["args"] = [*args]
            config.update(kwargs)
        super().__init__(config)

    @property
    def _args(self):
        """Return the ordered arguments.

        :return:
        :rtype: list
        """
        return [] if "args" not in self._config else self._config["args"]

    @property
    def _kwargs(self):
        """Return the default keyword arguments.

        :return:
        :rtype: dict
        """
        kwargs = self._config.copy()
        kwargs.pop("function")
        kwargs.pop("args", [])
        return kwargs

    @property
    def _f(self):
        """Return the imported function callable.

        :return:
        :rtype: typing.Callable
        """
        return self.import_function(self._config["function"])

    @staticmethod
    def import_function(name):
        """Import a function using its name.

        :param name:
        :return: function
        :rtype: typing.Callable
        """
        if name in imported_functions:
            # The function has already been imported
            return imported_functions[name]
        # Import the function
        LOGGER.debug("Importing function: {}".format(name))
        split_name = name.split(".")
        index = len(split_name) - 1
        module = None
        # Try to import the longest name as a module
        while module is None and index > 0:
            try:
                module_name = ".".join(split_name[:index])
                module = import_module(module_name)
            except ImportError:
                index -= 1
        prev = module
        # Load functions from module
        for part in split_name[index:]:
            prev = getattr(prev, part)
        func = prev
        imported_functions[name] = func
        return func

    def __call__(self, *args, **kwargs):
        up_args = [*args] + self._args[len(args) :]
        up_kwargs = self._kwargs.copy()
        up_kwargs.update(**kwargs)
        return self._f(*up_args, **up_kwargs)


class change_dir:
    """Context manager to temporarily move to another directory.

    :param path: path to get to
    :type path: str
    :param create: option to create path directories if they do not exist
    :type create: bool
    """

    def __init__(self, path, create=False):
        self.path = path
        self.create = create

    def __enter__(self):
        """Enter the defined path directory."""
        if self.create and os.path.isdir(self.path) is False:
            os.makedirs(self.path)
        self.old_path = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        """Go back to the old directory."""
        os.chdir(self.old_path)


def call_function(name, params):
    """Import and call a function.

    :param name:
        The name of the function to import, with its modules
        separated by dots, for example 'numpy.random.normal'.
    :type name: str
    :param params: Named parameters to use when calling the function.
    :type params: dict
    :param mapping: Whether the params is a mapping or a list. Default: `True`.
    :type mapping: bool
    """
    if name in imported_functions:
        # The function has already been imported
        func = imported_functions[name]
    else:
        # Import the function
        LOGGER.debug("Importing function: {}".format(name))
        split_name = name.split(".")
        index = len(split_name) - 1
        module = None
        # Try to import the longest name as a module
        while module is None and index > 0:
            try:
                module_name = ".".join(split_name[:index])
                module = import_module(module_name)
            except ImportError:
                index -= 1
        prev = module
        # Load functions from module
        for part in split_name[index:]:
            prev = getattr(prev, part)
        func = prev
        imported_functions[name] = func
    if isinstance(params, dict):
        return func(**params)
    else:
        return func(*params)


def try_convert(string):
    """Convert the string value to a number.

    Tries to return the string as an int first, then as a float,
    else returns the string.

    :param string:
    :type string: str
    :rtype: int, float or str
    """
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string


def dict_list_to_list(dict_list, header=None):
    """Convert list of dict to list of list.

    :param dict_list:
    :type dict_list: list(dict)
    :param header: ordered keys indexing rows of `dict_keys`
    :type header: list
    :return:
    :rtype: list(list)

    .. note:: header is not included in resulting list
    """
    if len(dict_list) == 0:
        return [[]]
    header = [*dict_list[0].keys()] if header is None else header
    return [[dico[k] for k in header] for dico in dict_list]


def list_to_dict_list(list_, header):
    """Convert list of list to list of dict.

    :param list_:
    :type list_: list(list)
    :param header: ordered indexes of each row
    :type header: list
    :return:
    :rtype: list(OrderedDict)
    """
    return [OrderedDict(zip(header, row)) for row in list_]


def unflatten_dict(dico, separator="."):
    """Nest a flattened dictionary using separator to split layers.

    :param dico: a flattened dictionary
    :type dico: dict
    :param separator: key separator
    :type separator: str
    :return: fully nested dictionary unflattened
    :rtype: dict

    .. note::
        this works also with partially nested and fully nested dictionary
        (though it returns the same dictionary in the latter case)
    """
    res = dict()
    for k, v in dico.items():
        parts = k.split(separator)
        d = res
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = v if type(v) != dict else unflatten_dict(v, separator)
    return res


def relative_path(dir_from, path_to):
    """Return relative path going from a directory to the target path.

    :param dir_from: origin directory
    :type dir_from: str
    :param path_to: target path
    :type path_to: str
    :return:
    :rtype: str
    """
    f = Path(dir_from).absolute()
    t = Path(path_to).absolute()
    root = Path(os.path.commonpath([str(f), str(t)]))
    relative_from = f.relative_to(root)
    relative_to = t.relative_to(root)
    return (
        "" if f == root else "../" * len(str(relative_from).split("/"))
    ) + str(relative_to)


def call_parallel_functions(commands, nb_processes=1):
    """Call functions in parallel using a
    :class:`concurrent.futures.ProcessPoolExecutor` and return results.

    :param commands:
        list of all commands to run (each command is a list starting
        by the function to run followed by its arguments)
    :type commands: list(list)
    :param nb_processes: number of processes spawned in parallel
    :type nb_processes: int
    :return: results
    :rtype: list

    .. note:: all processes are run on the local machine
    """
    with ProcessPoolExecutor(max_workers=nb_processes) as executor:
        pool = [executor.submit(*command) for command in commands]
        results = [f.result() for f in pool]
    return results
