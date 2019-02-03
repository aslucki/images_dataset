import argparse
from collections import namedtuple
import json
from math import ceil
import logging
import os
import sys
import time

import flickrapi
import yaml


class Fetcher:
    def __init__(self, flickrapi_object: flickrapi.FlickrAPI):
        self.__flickrapi_object = flickrapi_object

    @staticmethod
    def __build_url(photo_info):
        try:
           url = 'https://farm{farm}.staticflickr.com/'\
                 '{server}/{id}_{secret}_m.jpg'.format(**photo_info)
           return url
        except KeyError as err:
            logging.error('Key not found: {}'.format(err))
        return None

    @staticmethod
    def __get_results_info(flickrapi_search_results):
        search_results_info =\
            namedtuple('search_results_info', 'pages_count photos_count')

        try:
            pages_count = flickrapi_search_results['photos']['pages']
            photos_count =\
                pages_count * flickrapi_search_results['photos']['perpage']
            return search_results_info(pages_count=pages_count,
                                       photos_count=photos_count)
        except KeyError as err:
            logging.error('Key not found: {}'.format(err))

        return None


    def __flickrapi_search(self, name, per_page, page):
        if type(name) is str:
            name = [name]
        return self.__flickrapi_object.photos.search(tags=name,
                                                     per_page=str(per_page),
                                                     page=page)

    def __search_results_to_urls(self, flickrapi_search_results: dict)\
            -> list:
        try:
            return list(map(lambda x: self.__build_url(x),
                            flickrapi_search_results['photos']['photo']))
        except KeyError as err:
            logging.error(err)

        return None

    def __merge_search_results(self, name, count, per_page):

        flickrapi_search_results =\
            self.__flickrapi_search(name, per_page, page=1)

        search_results_info = self.__get_results_info(flickrapi_search_results)
        if not search_results_info:
            logging.error('Invalid API reponse')
            return None

        if search_results_info.photos_count < count:
            info = {'available': search_results_info.photos_count,
                    'requested': count}
            logging.warning('There are not enough resources available. '
                             'Count: {available}, requested: {requested}.\n'
                             'Fetching {available} url(s).'.format(**info))

        count = min(search_results_info.photos_count, count)
        pages_to_search = ceil(count / per_page)

        urls = self.__search_results_to_urls(flickrapi_search_results)
        # Return results from the first page
        # if it has enough elements
        if pages_to_search == 1:
            return urls[:count]

        # Iterate through next available pages
        # if the first page is not enough
        for page in range(2, pages_to_search+1):
            flickrapi_search_results = \
                self.__flickrapi_search(name, per_page, page=page)
            urls.extend(self.__search_results_to_urls(flickrapi_search_results))

            # Pause to not exceed API quota
            time.sleep(2)

        return urls

    def __fetch_class(self, name, count):
        per_page = min(500, count)

        return self. __merge_search_results(name, count, per_page)

    def fetch(self, classes: list) -> dict:
        classes_urls = {}
        try:
            for class_info in classes:
                class_name = class_info['name']
                class_count = class_info['count']

                classes_urls[class_name] =\
                    self.__fetch_class(class_name, class_count)

                logging.info('Fetched {} urls for the {} class'
                             .format(len(classes_urls[class_name]),
                                     class_name))
        except KeyError as err:
            logging.error(err)
        except TypeError as err:
            logging.error(err)
        except KeyboardInterrupt:
            logging.info('Stopped by user')
            sys.exit()

        return classes_urls

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True,
                        help="Path to the configuration file.")
    parser.add_argument('--output_dir', required=True,
                        help="Path to the directory for storing results")
    parser.add_argument('--output_file_name', required=False)

    return parser.parse_args()

def load_config(path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

        return None

def main():
    args = parse_arguments()
    config = load_config(args.config)
    logging.basicConfig(level=logging.INFO)

    flickr = flickrapi.FlickrAPI(os.environ.get('API_KEY'),
                                 os.environ.get('API_SECRET'),
                                 format='parsed-json')
    fetcher = Fetcher(flickr)
    fetched_urls = fetcher.fetch(config['classes'])

    file_name = 'urls_data.json'
    if args.output_file_name:
        file_name = args.output_file_name

    with open(os.path.join(args.output_dir, file_name), 'w') as f:
        json.dump(fetched_urls, f)

if __name__ == "__main__":
    main()
