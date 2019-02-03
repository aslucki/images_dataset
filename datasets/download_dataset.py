import argparse
from collections import namedtuple
import json
from math import floor, log10
import logging
import os
from urllib.request import urlopen
from urllib.error import HTTPError

from tqdm import tqdm
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


def __collect_download_info(urls: list, dir_name):
    download_info = \
        namedtuple('download_info', 'downloaded expected')

    downloaded_files_count = len(os.listdir(dir_name))
    expected_files_count = len(urls)

    if expected_files_count != downloaded_files_count:
        logging.warning('Downloaded {} files while {} was expected'.format(
            downloaded_files_count, expected_files_count))

    return download_info(downloaded=downloaded_files_count,
                         expected=expected_files_count)


def download_single_class_images(urls: list, output_dir):
    digits = floor(log10(len(urls))) + 1

    for i, url in enumerate(tqdm(urls)):
        image_name = '{}.jpg'.format(str(i).zfill(digits))
        save_path = os.path.join(output_dir, image_name)

        if not download_image(url, save_path):
            logging.warning('Could not download image from {}'.format(url))

    return __collect_download_info(urls, output_dir)


def download_dataset(urls_data: dict, output_dir) -> list:
    download_summary = []
    for class_name, urls in urls_data.items():
        logging.info('Downloading images for the "{}" class'
                     .format(class_name))
        class_subdir = os.path.join(output_dir, class_name)
        if not os.path.exists(class_subdir):
            os.makedirs(class_subdir)

        download_info = download_single_class_images(urls, class_subdir)
        download_summary.append('Class {}: Downloaded: {} Expected: {}\n'
                                .format(class_name,
                                        download_info.downloaded,
                                        download_info.expected))
    return download_summary


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True,
                        help="Path to the directory for storing results")
    parser.add_argument('--input_file_name', required=True)
    parser.add_argument('--output_file_name', required=True)

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

    with open(os.path.join(args.output_dir, args.input_file_name), 'r') as f:
        urls_data = json.load(f)

    summary = download_dataset(urls_data, args.output_dir)
    with open(os.path.join(args.output_dir, args.output_file_name), 'w') as f:
        f.writelines(summary)


if __name__ == '__main__':
    main()

