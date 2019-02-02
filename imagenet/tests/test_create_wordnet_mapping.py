import os

from imagenet.create_wordnet_mapping import (create_word_to_wnid_dict,
                                             retrieve_available_synsets,
                                             retrieve_wordnet_mapping)


def get_data_path(filename):
    dirname = os.path.dirname(__file__)
    data_path = os.path.join(dirname, 'data', filename)

    return data_path


def get_data_url(filename):
    dirname = os.path.dirname(__file__)
    data_path = os.path.join('file://', dirname, 'data', filename)

    return data_path


def get_available_synsets():
    available_synsets = ['n02512053',
                         'n02084071',
                         'n03538037']

    return available_synsets


def get_wordnet_mapping():
    wordnet_mapping = {'n02512053': 'fish',
                       'n02084071': 'dog',
                       'n03538037': 'horse',
                       'n00002452': 'thing',
                       'n00002684': 'object'}
    return wordnet_mapping


def test_retrieve_available_synsets():
    data_path = get_data_path('available_synsets.txt')
    data_url = get_data_path('available_synsets.txt')

    available_synsets_from_path = \
        retrieve_available_synsets(data_path)
    available_synsets_from_url = \
        retrieve_available_synsets(data_url)

    assert available_synsets_from_path == get_available_synsets()
    assert available_synsets_from_url == get_available_synsets()


def test_retrieve_wordnet_mapping():
    data_path = get_data_path('wordnet_mapping.txt')
    data_url = get_data_path('wordnet_mapping.txt')

    wordnet_mapping_from_path = \
        retrieve_wordnet_mapping(data_path)
    wordnet_mapping_from_url = \
        retrieve_wordnet_mapping(data_url)

    print(wordnet_mapping_from_path)

    assert wordnet_mapping_from_path == get_wordnet_mapping()
    assert wordnet_mapping_from_url == get_wordnet_mapping()


def test_create_word_to_wnid_dict():
    available_synsets = get_available_synsets()
    wordnet_mapping = get_wordnet_mapping()

    word_to_wnid_dict = create_word_to_wnid_dict(wordnet_mapping,
                                                 available_synsets)
    assert word_to_wnid_dict['fish'] == 'n02512053'
    assert word_to_wnid_dict['dog'] == 'n02084071'
    assert word_to_wnid_dict['horse'] == 'n03538037'
    assert 'thing' not in word_to_wnid_dict.keys()
    assert 'object' not in word_to_wnid_dict.keys()





