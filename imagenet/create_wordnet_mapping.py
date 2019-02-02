import json
import os

import utils

def __parse_raw_entry(raw_entry):
    try:
        parsed = raw_entry.decode('utf-8').rstrip()
    except AttributeError:
        parsed = raw_entry.rstrip()

    return parsed

def retrieve_available_synsets(available_synsets_uri):
    available_synsets = \
        utils.load_document(available_synsets_uri)

    return [__parse_raw_entry(wordnet)
            for wordnet in available_synsets]

def retrieve_wordnet_mapping(wordnet_mapping_uri) -> dict:
    wordnet_mapping = utils.load_document(wordnet_mapping_uri)

    wnid_to_word = {}
    for entry in wordnet_mapping:
        data = __parse_raw_entry(entry).split('\t')
        wnid = data[0]
        top_word = data[1].split(',')[0].lower()
        wnid_to_word[wnid] = top_word

    return wnid_to_word


def create_word_to_wnid_dict(wordnet_mapping, available_synsets) -> dict:

    return {word:wnid for wnid, word in wordnet_mapping.items()
            if wnid in available_synsets }


def main():
    args = utils.parse_arguments()
    config = utils.load_config(args.config)

    available_synsets =\
        retrieve_available_synsets(config['available_synsets'])
    wordnet_mapping = retrieve_wordnet_mapping(config['wordnet_mapping'])

    word_to_wnid = create_word_to_wnid_dict(wordnet_mapping,
                                            available_synsets)

    with open(os.path.join('outputs', 'wordnet_mapping.json'), 'w') as f:
        json.dump(word_to_wnid, f)

if __name__ == "__main__":
    main()






