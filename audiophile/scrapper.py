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


def create_data_folders(path):
    """
    I create destination pages cache and audio files folders.

    Args:
        path (str): folder path
    Returns:
        None.
    """
    try:
        # path doesn't exists: create data folders
        if not os.path.exists(path):

            # create base folder
            os.mkdir(path)

            # create pages cache folder
            os.mkdir(path + 'pages/')
            os.mkdir(path + 'pages/indexes/')
            os.mkdir(path + 'pages/results/')

            # create audio files folder
            os.mkdir(path + 'audio/')

    # couldn't create folders: abort and report error
    except OSError:
        print(f"Error: couldn't create folder {path} .")


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

    # create data and pages cache destination folder
    create_data_folders('./data/')
