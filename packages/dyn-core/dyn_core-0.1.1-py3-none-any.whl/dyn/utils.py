"""Utilities module

Contains helper functions and file saving/loading functions.
"""
from __future__ import annotations

import logging
import os
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from networkx import Graph

__all__ = ["undirected_graphs_equal"]


imported_functions = {}


LOGGER = logging.getLogger(__name__)


def undirected_graphs_equal(graph1: Graph, graph2: Graph) -> bool:
    """Check if two undirected graphs have same nodes/edges.

    :param graph1:
    :param graph2:
    :return:
    """
    if set(graph1.nodes) != set(graph2.nodes):
        return False
    gr_edges1 = graph1.edges
    gr_edges2 = graph2.edges
    for u, v in gr_edges1:
        if (u, v) not in gr_edges2:
            return False
    for u, v in gr_edges2:
        if (u, v) not in gr_edges1:
            return False
    return True


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
