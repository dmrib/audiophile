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


BASE_URL = 'https://freesound.org'
SEARCH_QUERY = 'https://freesound.org/search/?q={}&page={}#sound'
TAGS_QUERY = 'https://freesound.org/browse/tags/{}/?page={}#sound'
INDEX_FILE_NAME = 'index_{}.html'
SOUND_FILE_NAME = 'sound_page_{}.html'


def get_page(url):
    """
    Download a web page and returns it.

    Args:
        url (str): target webpage url
    Returns:
        html (str): page html code
    """
    # request HTML page
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
    # save HTML page
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
    print('\nScraping indexes...')
    for page_number in tqdm(range(1, n_pages + 1)):
        url = base_url.format(query, page_number)
        page = get_page(url)
        save_page(page, destination + INDEX_FILE_NAME.format(page_number))


def parse_indexes(source_folder, destination):
    """
    Parses pages in a folder for audio pages urls and store in a csv
    file.

    Args:
        source_folder (str): index pages source folder
        destination (str): destination path for csv file.
    Returns:
        None.
    """
    # get search results pages files paths
    pages_file_names = glob.glob(source_folder + '*.html')

    # parse search results pages for sound files pages and creates csv
    print('\nParsing indexes pages...')
    with open(destination + '/sound_pages_urls.csv', mode='w') as urls_file:
        writer = csv.writer(urls_file)

        for page_file_name in tqdm(pages_file_names):
            with open(page_file_name, mode='r') as page_file:
                soup = BeautifulSoup(page_file, 'lxml')

                for url in soup.findAll('a', attrs={'class': 'title'}):
                    page_url = [BASE_URL + url.get('href')]
                    writer.writerow(page_url)


def scrape_sound_pages(pages_file_path, destination):
    """
    Scrapes sound track pages.

    Args:
        pages_file_path (str): path of urls source file.
        destination (str): destination path for scrapped pages.
    Returns:
        None.
    """
    # get url list from csv file
    with open(pages_file_path, 'r') as urls_file:
        reader = csv.reader(urls_file)
        urls = list(reader)

    # scrape sound track pages
    n = 1
    print('\nScraping sound pages...')
    for url in tqdm(urls):
        page = get_page(url[0])
        save_page(page, destination + SOUND_FILE_NAME.format(n))
        n += 1


def parse_sound_pages(source_folder, destination):
    """
    Parses a sound file pages collection and create a csv file of sounds files
    download urls.

    Args:
        source_folder (str): sounds files pages folder.
        destination (str): destination path for csv file.
    Returns:
        None.
    """
    # get pages files paths
    pages_files_names = glob.glob(source_folder + '*.html')

    # parse sound pages for sound download links
    print('\nParsing sound pages...')
    with open(destination + 'download_urls.csv', mode='w') as urls_file:
        writer = csv.writer(urls_file)

        for page_file_name in tqdm(pages_files_names):
            with open(page_file_name, mode='r') as page_file:
                soup = BeautifulSoup(page_file, 'lxml')
                download_link = soup.find('div', attrs={'id':'download'})\
                                    .a.get('href')
                download_link = BASE_URL + download_link
                writer.writerow([download_link])


def download_sound_files(urls_source, formats, auth, destination):
    """
    Downloads sound files.

    Args:
        urls_file (str): path of csv containing file urls.
        formats (list): desired file formats.
        auth (dict): access cookies.
        destination (str): files destination folder path.
    Returns:
        None.
    """
    # get urls
    with open(urls_source) as urls_file:
        reader = csv.reader(urls_file)
        urls = list(reader)

    # download audio files
    n = 1
    print('\nDownloading audio files....')
    for url in tqdm(urls):
        format = url[0].split('.')[-1]
        if format in formats:
            audio = requests.get(url[0],
                                 cookies= {
                                            'csrftoken': auth['csrf'],
                                            'sessionid': auth['session']
                                          })
            with open(destination + f'sound{n}.{format}', mode='wb') as file:
                file.write(audio.content)
                n += 1


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

    # create data and pages cache destination folders
    base_folder = '../data/{}/'.format(parameters['query'])
    indexes_folder = base_folder + 'pages/indexes/'
    sounds_pages_folder = base_folder + 'pages/results/'
    audio_folder = base_folder + 'audio/'
    create_data_folders(base_folder)

    # scrape search results pages
    scrape_indexes(parameters['query'], parameters['query_type'],
                   parameters['n_pages'], indexes_folder)

    # parse search results pages for sound files pages
    parse_indexes(indexes_folder, base_folder)

    # scrape sound files pages
    scrape_sound_pages(base_folder + 'sound_pages_urls.csv',
                       sounds_pages_folder)

    # parse sound pages
    parse_sound_pages(sounds_pages_folder, base_folder)

    # download sounds
    download_sound_files(base_folder + 'download_urls.csv',
                         parameters['formats'], parameters['auth'],
                         audio_folder)


if __name__ == '__main__':
    scrape('../config.json')
