import argparse
from collections import defaultdict
import json
import logging
import os
import random

from jsonschema import validate
import yaml


def __get_schema():
    schema = {
        "type": "object",
        "properties": {
            "train": {"type": "array",
                      "items":
                          {"type": "string"}
                      },
            "test": {"type": "array",
                     "items":
                         {"type": "string"}
                     }
        },
        "additionalProperties": False
    }
    return schema


def __paths_to_classes(paths: dict) -> dict:

    classes = defaultdict(list)
    for entry in paths:
        class_ = os.path.dirname(entry)
        file_name = os.path.basename(entry)
        classes[class_].append(file_name)

    return classes


def __extract_subset(classes: dict, percentage: float, seed=42) -> dict:

    if percentage > 100 or percentage < 0:
        raise ValueError('Percentage should be between 0 and 100')
    elif percentage > 1:
        percentage /= 100.

    subset = {}
    for class_, file_names in classes.items():
        random.seed(seed)
        random.shuffle(file_names)

        subset_size = int(len(file_names) * percentage)
        logging.info('Extracting {} samples from the "{}" class'
                     .format(subset_size, class_))
        subset[class_] = file_names[:subset_size]

    return subset


def __classes_to_paths(classes: dict) -> list:

    paths = []
    for class_, file_names in classes.items():
        paths.extend(
            list(map(lambda x: os.path.join(class_, x), file_names))
        )

    return paths


def __process_split(split: list, percentage, seed):
    classes = __paths_to_classes(split)
    subset = __extract_subset(classes, percentage, seed)
    paths = __classes_to_paths(subset)

    return paths


def extract(train_test_split, percentage, seed):
    try:
        validate(train_test_split, __get_schema())
    except ValueError:
        logging.error('Input file is not formatted correctly')

    dataset = {}
    for key in train_test_split.keys():
        dataset[key] = \
            __process_split(train_test_split[key],
                            percentage, seed)
    return dataset


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True,
                        help="Path to the configuration file.")
    parser.add_argument('--input_file_name', required=True)
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


def main():
    args = parse_arguments()
    config = load_config(args.config)
    logging.basicConfig(level=logging.INFO)

    with open(os.path.join(args.output_dir, args.input_file_name), 'r') as f:
        dataset = json.load(f)

    subset = extract(dataset, config['subset']['percentage'],
                     config['subset']['seed'])

    with open(os.path.join(args.output_dir, args.output_file_name), 'w') as f:
        json.dump(subset, f, indent=4)


if __name__ == "__main__":
    main()

