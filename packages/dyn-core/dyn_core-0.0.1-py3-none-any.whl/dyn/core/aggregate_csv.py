"""This script aggregates csv files that share the same column names.

.. code:: bash

    usage: aggregate_csv.py [-h] [-o OUTPUT] [--label LABEL] files [files ...]

    Aggregate multiple CSV files

    positional arguments:
    files                 CSV files to aggregate

    options:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            CSV file in which to write result
    --label LABEL         Column label containing aggregated file original path
"""
import pandas as pd

from dyn._utils import relative_path
from dyn.core.files_io import load_csv, save_csv

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Aggregate multiple CSV files"
    )
    parser.add_argument(
        "files", type=str, nargs="+", help="CSV files to aggregate"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="aggregation.csv",
        help="CSV file in which to write result",
    )
    parser.add_argument(
        "--label",
        type=str,
        default="dataset",
        help="Column label containing aggregated file original path",
    )

    args = parser.parse_args()

    columns = None

    for file in args.files:
        rows = load_csv(file)
        df = pd.DataFrame(rows[1:], columns=rows[0])
        name = relative_path(args.output, file)
        if not columns:
            columns = [args.label] + df.columns.tolist()
            save_csv([columns], args.output)
        df[args.label] = name
        df = df[columns]
        save_csv(df.values.tolist(), args.output, append=True)
