import json

from os.path import exists, isdir
from os import makedirs
from pathlib import Path


def check_exists_dir(path_dir):
    """
    Check exists dir

    :param path_dir: the path to the dir
    :type path_dir: string
    """
    if not isdir(path_dir):
        raise Exception(f'Not found dir "{path_dir}"')


def check_exists_create_path(path):
    """
    Check exists and create path

    :param path:
    :return:
    """
    if not isdir(path):
        makedirs(path)


def check_exists_file(path_file):
    """
    Check exists file

    :param path_file: the path to the file
    :type path_file: string
    """
    if not exists(path_file):
        _path = Path(path_file)
        raise FileNotFoundError('Not found file "{0}"'.format(_path.name))


def load_config(filename_config):
    """
    Loading configuration

    :param filename_config: the path to the configuration file
    :type filename_config: string
    :return: configuration
    :return type: dictionary
    """
    try:
        check_exists_file(filename_config)
        with open(filename_config, encoding='utf-8') as fh:
            config = json.load(fh)
        return config
    except IOError as exc:
        raise RuntimeError('Failed to load file config') from exc


def save_data(data, path, header=True, sep=';', decimal='.', index=False
              , encoding='cp1251', na_rep='Nan', float_format='%.4f', date_format='%Y%m%d'):
    '''

    :param data:
    :param path:
    :param header:
    :param sep:
    :param decimal:
    :param index:
    :param encoding:
    :param na_rep:
    :param float_format:
    :return:
    '''
    try:
        data.to_csv(path_or_buf=path, header=header, decimal=decimal
                    , sep=sep, index=index, na_rep=na_rep, encoding=encoding
                    , float_format=float_format, date_format=date_format)
    except Exception as exc:
        raise Exception(f'Error while saving data to file') from exc