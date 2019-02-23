"""
Web pages and audio files scrapper.
"""

import csv
import glob
import json
import os
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm


def load_config(path):
    """
    Loads a scrapping session configuration parameters from a JSON file.

    Args:
        path (str): path of configuration file.
    Returns:
        config (dict): scrapping session configuration parameters.
    """
    # open configuration file, load and return it
    with open(path) as config_file:
        config = json.loads(config_file.read())
        return config


def scrape(config_path):
    """
    Runs a scrapping session.

    Args:
        config_path (str): path of session JSON configuration file.
    Returns:
        None.
    """
    # load session parameters
    parameters = load_config(config_path)
