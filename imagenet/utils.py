import argparse
from urllib.request import urlopen

import yaml


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True,
                        help="Path to the configuration file.")

    return parser.parse_args()


def load_config(path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

        return None


def load_document(document_uri):
    try:
        document = urlopen(document_uri).readlines()

    except ValueError:
        with open(document_uri, 'r') as f:
            document = f.readlines()

    return document
