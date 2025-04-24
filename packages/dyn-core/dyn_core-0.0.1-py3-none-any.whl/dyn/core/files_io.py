import configparser
import csv
import json
from pathlib import Path

import nbformat as nbf
import networkx as nx
import tomli
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from pandas import DataFrame

from dyn._utils import try_convert, unflatten_dict
from dyn.core.communities import Tcommlist


class DataDialect(csv.Dialect):
    """Datadialect used to read tcommlist files."""

    delimiter = ","
    doublequote = True
    escapechar = None
    lineterminator = "\r\n"
    quotechar = '"'
    quoting = csv.QUOTE_NONNUMERIC
    skipinitialspace = False
    strict = True


csv.register_dialect("datadialect", DataDialect)


def save_graph(graph, filename):
    """Save graph in gml format.

    :param graph: any graph structure
    :type graph: nx.Graph
    :param filename:
    :type filename: str
    """
    nx.write_gml(graph, filename)


def load_graph(filename):
    """Load graph in gml file.

    :param filename:
    :type filename: str
    :return: graph
    :rtype: nx.Graph
    """
    return nx.read_gml(filename)


def load_csv(filename):
    """Load csv file.

    :param filename:
    :type filename: str
    :return: list of objects
    :rtype: list(list)

    .. note:: It will try to convert numbers to int when possible
    """

    def try_convert_to_int(value):
        if not isinstance(value, float) or int(value) != value:
            return value
        return int(value)

    res = []
    with open(filename, "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile, dialect="datadialect")
        for row in csvreader:
            res.append([try_convert_to_int(v) for v in row])
    return res


def save_csv(list_, filename, append=False):
    """Save as csv file.

    :param list_:
    :type list_: list(list)
    :param filename:
    :type filename: str
    :param append: if ``True`` appends to the file instead of overwriting
    :type append: bool
    """
    mode = "a" if append else "w"
    output_file = Path(filename)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(filename, mode, newline="") as csvfile:
        writer = csv.writer(csvfile, dialect="datadialect")
        writer.writerows(list_)


def load_tcommlist(filename: str) -> Tcommlist:
    """Load tcommlist file.

    :param filename:
    :return: tcommlist
    """
    return Tcommlist(DataFrame(load_csv(filename)[1:]))


def save_tcommlist(tcommlist: Tcommlist, filename: str):
    """Save tcommlist file.

    :param tcommlist:
    :param filename:
    """
    df = DataFrame(tcommlist)
    save_csv([df.columns.tolist()] + df.values.tolist(), filename)


def load_commlist(filename: str) -> Tcommlist:
    """Load commlist file.

    :param filename:
    :return: tcommlist
    """
    return Tcommlist(DataFrame(load_csv(filename)))


def save_commlist(commlist: Tcommlist, filename: str):
    """Save commlist file.

    :param commlist:
    :param filename:

    .. note:: same as :func:`save_tcommlist` but don't include headers
    """
    df = DataFrame(commlist)
    save_csv(df.values.tolist(), filename)


def load_json(filename):
    """Load json file.

    :param filename:
    :type filename: str
    :rtype: dict
    """
    with open(filename, "rb") as f:
        return json.load(f)


def save_json(dico: dict, filename: str):
    """Save to json file.

    :param dico:
    :param filename:
    """
    with open(filename, "w") as f:
        json.dump(dico, f)


def load_toml(filename):
    """Load TOML configuration file.

    :param filename:
    :type filename: str
    :rtype: dict
    """
    with open(filename, "rb") as f:
        return tomli.load(f)


def load_ini(filename, convert_numeric=True):
    """Load INI configuration file.

    :param filename:
    :type filename: str
    :rtype: dict
    """
    parser = configparser.ConfigParser()
    parser.read(filename)
    res = {k: dict(v) for k, v in dict(parser).items()}
    if not convert_numeric:
        return res
    for k1 in res:
        for k2 in res[k1]:
            res[k1][k2] = try_convert(res[k1][k2])
    return res


def load_config(filename):
    """Load a configuration file.

    Configuration file is assumed as a potentially nested configuration file.

    :param filename:
    :type filename: str
    :rtype: dict
    :raise ValueError: if an unsupported format is used

    .. note::
        .ini file will be unflatten and their attributes converted to numeric
        value when possible
    """
    ext = filename.split(".")[-1]
    if ext == "ini":
        return unflatten_dict(load_ini(filename))
    elif ext == "toml":
        return load_toml(filename)
    elif ext == "json":
        return load_json(filename)
    else:
        raise ValueError(f"unsupported config file extension: {ext}")


def load_notebook(filename):
    """Load a notebook.

    :param filename:
    :type filename: str
    :return: loaded notebook
    :rtype: nbf.NotebookNode
    """
    with open(filename) as f:
        return nbf.read(f, as_version=4)


def save_notebook(notebook, filename):
    """Save a notebook.

    :param notebook:
    :type notebook: nbf.NotebookNode
    :param filename:
    :type filename: str
    """
    with open(filename, "w", encoding="utf-8") as f:
        nbf.write(notebook, f)


def save_notebook_html(
    notebook, filename, exclude_input=False, **conversion_kargs
):
    """Save a notebook in HTML format.

    :param notebook:
    :type notebook: nbf.NotebookNode
    :param filename:
    :type filename: str
    :param exclude_input:
        ``True`` for excluding cell inputs from resulting HTML file
    :type exclude_input: bool
    :param conversion_kargs:
        kwargs for the :class:`nbconvert.HTMLExporter` constructor
    """
    html_exporter = HTMLExporter(
        exclude_input=exclude_input, **conversion_kargs
    )
    html_data, _ = html_exporter.from_notebook_node(notebook)
    with open(filename, "w") as f:
        f.write(html_data)


def execute_notebook(notebook, execution_path=None):
    """Execute a notebook.

    :param notebook:
    :type notebook: nbf.NotebookNode
    :param execution_path:
        path from which to execute notebook (default ``"."``)
    :type execution_path: str
    """
    execution_path = "." if execution_path is None else execution_path
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(notebook, {"metadata": {"path": execution_path}})
