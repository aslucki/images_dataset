import os
import tempfile

from download_dataset import download_image


def get_data_url(filename):
    dirname = os.path.dirname(__file__)
    data_path = os.path.join('file://', dirname, 'data', filename)

    return 'file://' + data_path


def test_download_image_valid():
    url = get_data_url('image_1.jpg')

    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = os.path.join(temp_dir, 'image.jpg')
        result = download_image(url, save_path)

    assert result is True


def test_download_image_invalid():
    url = get_data_url('image.jpg')

    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = os.path.join(temp_dir, 'image.jpg')
        result = download_image(url, save_path)

    assert result is False
