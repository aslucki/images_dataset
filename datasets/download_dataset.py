import argparse
import json
import logging
import os
from urllib.request import urlopen
from urllib.error import HTTPError

from progressbar import progressbar
import yaml

def download_image(url, save_path):
    try:
        resp = urlopen(url)
        with open(save_path, 'wb') as f:
            f.write(resp.read())
            return True

    except HTTPError as err:
        logging.error('Connection error: {}'.format(err))

    except IOError as err:
        logging.error('File error: {}'.format(err))

    return False


def download_single_class_images(urls: list, output_dir):
    for i, url in enumerate(urls):
        save_path = os.path.join(output_dir, '{0:05d}.jpg'.format(i))

        if download_image(url, save_path) is False:
            logging.warning('Could not download image from {}'.format(url))

def download_dataset(urls_data: dict, output_dir):
    for class_name, urls in urls_data.items():
        logging.info('Downloading images for the "{}" class'
                     .format(class_name))
        class_subdir = os.path.join(output_dir, class_name)
        if not os.path.exists(class_subdir):
            os.makedirs(class_subdir)

        download_single_class_images(urls, class_subdir)
        downloaded_files_count = len(os.listdir(class_subdir))
        expected_files_count = len(urls)

        if expected_files_count != downloaded_files_count:
            logging.warning('Downloaded {} files while {} was expected'.format(
                downloaded_files_count, expected_files_count ))
        logging.info("Downdloaded {} images for the {} class".format(downloaded_files_count,
                                                                     class_name))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True,
                        help="Path to the directory for storing results")
    parser.add_argument('--input_file_name', required=True)

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
    logging.basicConfig(level=logging.INFO)

    file_name = 'urls_data.json'
    if args.input_file_name:
        file_name = args.input_file_name

    with open(os.path.join(args.output_dir, file_name), 'r') as f:
        urls_data = json.load(f)

    download_dataset(urls_data, args.output_dir)

if __name__ == '__main__':
    main()

