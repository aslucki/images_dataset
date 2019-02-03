import argparse
from collections import namedtuple
import json
import logging
import os
import random

import yaml

class Splitter:

    def __init__(self, test_size, type, seed):
        self.__test_size = self.__set_test_size(test_size, type)
        self.__seed = seed

    @staticmethod
    def __set_test_size(test_size, type):
        if type.lower() == 'absolute':
            return int(test_size)
        elif type.lower() == 'proportional':
            if test_size > 1:
                test_size /= 100
            elif test_size > 100:
                raise ValueError('Percentage size cannot be greater than 100')

            calculated_size = int(len(__file_names) * test_size)

            return calculated_size


    def __split_single_class(self, parent_dir_name: str, class_dir_name: str):
        file_names = os.listdir(os.path.join(parent_dir_name, class_dir_name))
        random.seed(self.__seed)
        random.shuffle(file_names)
        data_split = namedtuple('data_split', 'train test')

        return data_split(train=file_names[self.__test_size:],
                          test=file_names[:self.__test_size])

    def __join_paths(self, class_dir_name, file_names):
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

        return {'train': train, 'test':test}

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

    splitter = Splitter(config['train_test_split']['test_size'],
                        config['train_test_split']['type'],
                        config['train_test_split']['seed'])

    class_dir_names = [class_info['name']
                       for class_info in config['classes']]

    train_test_split = splitter.split_dataset(args.output_dir, class_dir_names)

    file_name = 'train_test_split.json'
    if args.output_file_name:
        file_name = args.output_file_name

    with open(os.path.join(args.output_dir, file_name), 'w') as f:
        json.dump(train_test_split, f)

if __name__ == '__main__':
    main()