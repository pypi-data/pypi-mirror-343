SEP005 24SEA parquet io
-----------------------

Basic package to import data from parquet files as stored by 24SEA's SHM solutions.

Using the package
------------------

    .. code-block:: python

        from sep005_io_parquet import read_parquet

        file_path = # Path to the parquet file of interest
        signals = read_parquet(file_path)

Acknowledgements
----------------
