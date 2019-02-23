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


SEARCH_QUERY = 'https://freesound.org/search/?q={}&page={}#sound'
TAGS_QUERY = 'https://freesound.org/browse/tags/{}/?page={}#sound'
INDEX_FILE_NAME = 'index_{}.html'


def get_page(url):
    """
    Download a web page and returns it.

    Args:
        url (str): target webpage url
    Returns:
        html (str): page html code
    """
    response = requests.get(url)
    html = response.text

    return html


def save_page(page, file_name):
    """
    I save a page to a file.

    Args:
        page (str): page to be saved.
        file_name (str): saved file name.
    Returns:
        None.
    """
    with open(file_name, mode='w') as file:
        file.write(page)


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


def scrape_indexes(query, query_type, n_pages, destination):
    """
    Scraps search results pages.

    Args:
        query (str): query word
        query_type (str): type of audio files query.
        n_pages (int): number of pages to scrape.
        destination (str): scrapped pages destination folder path.
    Returns:
        None.
    """
    # select query results base url
    if query_type == 'search':
        base_url = SEARCH_QUERY
    elif query_type == 'tags':
        base_url = TAGS_QUERY

    # scrape search result pages
    print('Scraping indexes...')
    for page_number in tqdm(range(1, n_pages + 1)):
        url = base_url.format(query, page_number)
        page = get_page(url)
        save_page(page, destination + INDEX_FILE_NAME.format(page_number))


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
    base_folder = '../data/{}/'.format(parameters['query'])
    indexes_folder = base_folder + 'pages/indexes/'
    create_data_folders(base_folder)

    # scrape search results pages
    scrape_indexes(parameters['query'], parameters['query_type'],
                   parameters['n_pages'], indexes_folder)
