import argparse
from collections import namedtuple
import json
import logging
import os
import random

import yaml


class Splitter:

    def __init__(self, test_size, split_type, seed):
        self.__split_type = split_type.lower()
        self.__test_size = self.__set_test_size(test_size)
        self.__seed = seed

    def __set_test_size(self, test_size):
        if self.__split_type == 'absolute':
            return int(test_size)
        elif self.__split_type == 'proportional':
            if test_size > 1:
                test_size /= 100
            elif test_size > 100 or test_size < 0:
                raise ValueError('Percentage size must be between 0-100')

            return test_size

    def __split_single_class(self, parent_dir_name: str, class_dir_name: str):
        file_names = os.listdir(os.path.join(parent_dir_name, class_dir_name))
        random.seed(self.__seed)
        random.shuffle(file_names)
        data_split = namedtuple('data_split', 'train test')

        test_size = self.__test_size
        if self.__split_type == 'proportional':
            test_size = int(len(file_names) * test_size)

        return data_split(train=file_names[test_size:],
                          test=file_names[:test_size])

    @staticmethod
    def __join_paths(class_dir_name, file_names):
        return list(map(lambda file_name:
                        os.path.join(class_dir_name, file_name),
                        file_names))

    def split_dataset(self, parent_dir_name: str,
                      class_dir_names: list) -> dict:

        train = []
        test = []
        for class_dir_name in class_dir_names:
            data_split = self.__split_single_class(parent_dir_name, class_dir_name)
            train.extend(self.__join_paths(class_dir_name, data_split.train))
            test.extend(self.__join_paths(class_dir_name, data_split.test))

        return {'train': train, 'test': test}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True,
                        help="Path to the configuration file.")
    parser.add_argument('--output_dir', required=True,
                        help="Path to the directory for storing results")
    parser.add_argument('--output_file_name', required=True)

    return parser.parse_args()


def load_config(path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

        return None


def get_classes_names(output_dir, config):
    class_dir_names = next(os.walk(output_dir))[1]
    if type(class_dir_names) is not list:
        class_dir_names = [class_dir_names]
    class_config_names = [entry['name'] for entry in config['classes']]

    difference = set(class_dir_names).\
        symmetric_difference(class_config_names)
    if len(difference) != 0:
        logging.warning('There is a mismatch between '
                        'subdirectories names and '
                        'classes defined in the config:\n'
                        .format(difference))

    return class_dir_names


def main():
    args = parse_arguments()
    config = load_config(args.config)
    logging.basicConfig(level=logging.INFO)

    splitter = Splitter(config['train_test_split']['test_size'],
                        config['train_test_split']['type'],
                        config['train_test_split']['seed'])

    class_dir_names = get_classes_names(args.output_dir, config)

    train_test_split = splitter.split_dataset(args.output_dir,
                                              class_dir_names)

    with open(os.path.join(args.output_dir, args.output_file_name), 'w') as f:
        json.dump(train_test_split, f, indent=4)


if __name__ == '__main__':
    main()
