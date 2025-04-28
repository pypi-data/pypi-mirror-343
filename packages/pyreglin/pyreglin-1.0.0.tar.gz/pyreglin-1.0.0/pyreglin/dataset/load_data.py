import os

from urllib.request import urlopen
import pandas as pd


DATASET_SOURCE = "https://raw.githubusercontent.com/salvnetto/pyreglin/refs/heads/main/pyreglin/dataset/datasets/"
DATASET_NAMES_URL = f"{DATASET_SOURCE}/dataset_names.txt"


def get_dataset_names() -> list:
    """
    Report available example datasets.

    Requires an internet connection.
    """
    with urlopen(DATASET_NAMES_URL) as response:
        txt = response.read()
        
    dataset_names = [name.strip() for name in txt.decode().split("\n")]
    return list(filter(None, dataset_names))


def load_data(
        dataset_name: str,
        **kwargs
    ) -> pd.DataFrame:
    """Load an example dataset.

    Use :func:`get_dataset_names` to see a list of available datasets.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset ``{name}``.
    kwargs : keys and values, optional
        Additional keyword arguments are passed to passed through to
        :func:`pandas.read_csv`.

    Returns
    -------
    pandas.DataFrame

    """
    if not isinstance(dataset_name, str):
        error = (
            """
            This function accepts only strings (the name of an example dataset). 
            Please use get_dataset_names() to see a list of available datasets.
            """
        )
        raise TypeError(error)
    base_file = __file__
    filepath = os.path.dirname(os.path.abspath(base_file)) + "\\datasets\\"
    filename = os.path.join(filepath, dataset_name) + ".csv"
    data = pd.read_csv(filename, **kwargs)
    return data
