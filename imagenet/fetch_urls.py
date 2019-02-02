import json
import os
import logging

import utils


class Fetcher:
    def __init__(self, wordnet_mapping_path, api_url):
        self.__wordnet_mapping = self.__load_mapping(wordnet_mapping_path)
        self.__api_url = api_url

    @staticmethod
    def __load_mapping(mapping_path):
        with open(mapping_path, 'r') as f:
            return json.load(f)

    def __fetch_class(self, word):
        url = self.__build_url(word)
        images_urls = utils.load_document(url)

        return [image_url.decode('utf-8').rstrip()
                for image_url in images_urls]

    def __build_url(self, word):
        wnid = self.__wordnet_mapping.get(word)
        if wnid:
            url = '{}?wnid={}'.format(self.__api_url, wnid)
            return url
        return None

    def fetch(self, classes: list) -> dict:
        classes_urls = {}
        for class_name in classes:
            classes_urls[class_name] =\
                self.__fetch_class(class_name)

            logging.info('Fetched {} urls for the {} class'
                         .format(len(classes_urls[class_name]),
                                 class_name))

        return classes_urls


def main():
    args = utils.parse_arguments()
    config = utils.load_config(args.config)
    logging.basicConfig(level=logging.INFO)

    fetcher = Fetcher(os.path.join('outputs', 'wordnet_mapping.json'),
                      config['urls_by_wnid'])

    classes_dict = fetcher.fetch(config['classes_to_fetch'])

    with open(os.path.join('outputs', 'fetched_urls.json'), 'w') as f:
        json.dump(classes_dict, f)


if __name__ == "__main__":
    main()
