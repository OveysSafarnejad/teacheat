# -*- coding: utf-8 -*-
"""
core utils module.
"""
import datetime
import os
import shutil
import zipfile

import requests
from django.conf import settings

from apps.core.validators import is_valid_mobile


def make_iterable(values, collection=None):
    """
    converts the provided values to iterable.

    it returns a collection of values using the given collection type.

    :param object | list[object] | tuple[object] | set[object] values: value or values to make
                                                                       iterable. if the values
                                                                       are iterable, it just
                                                                       converts the collection
                                                                       to given type.

    :param type[list | tuple | set] collection: collection type to use.
                                                defaults to list if not provided.

    :rtype: list | tuple | set
    """

    if collection is None:
        collection = list

    if values is None:
        return collection()

    if not isinstance(values, (list, tuple, set)):
        values = (values,)

    return collection(values)


def create_directory(path, ignore_existed=False):
    """
    create a directory in given path.

    :param str path: path to create directory.

    :param bool ignore_existed: ignore if directory is already existed.
                                defaults to False if not provided an raises an error.

    :rtype: str
    """

    os.makedirs(path, exist_ok=ignore_existed)


def create_file(path, text):
    """
    creates a file with given text in given path.

    :param str path: file path.
    :param str text: text to create file from it.
    """

    with open(path, mode='w') as file:
        file.write(text)


def remove_directory(path):
    """
    removes the given directory.

    :param str path: directory path.
    """

    shutil.rmtree(path, ignore_errors=True)


def create_zip_file(directory):
    """
    creates a zip file from given directory.

    it places the zip file beside the input directory.
    it returns the full path of generated file.

    :param str directory: directory path.

    :rtype: str
    """

    full_name = '{directory}.zip'.format(directory=directory)
    with zipfile.ZipFile(full_name, mode='w') as file:
        for root, folders, files in os.walk(directory):
            for item in files:
                file_path = os.path.join(root, item)
                file.write(file_path, os.path.basename(file_path))

    return full_name


def split_name(full_path):
    """
    gets the root path and the name of the source directory or file.

    :param str full_path: full file or directory path.

    :returns: tuple[str root, str name]
    :rtype: tuple[str, str]
    """

    # this is to ensure that path does not end with '/'.
    full_path = full_path.rstrip(os.path.sep).rstrip(os.path.altsep)
    parts = os.path.split(full_path)
    root = os.path.join(*parts[0:-1])
    return root, parts[-1]


def get_file_extension(file, **options):
    """
    gets the extension of given file.

    :param str file: file path to get its extension.

    :keyword bool remove_dot: specifies that the extension must not
                              include the `.` character.
                              defaults to True if not provided.

    :keyword bool lowercase: specifies that extension must be changed to lowercase.
                             defaults to True if not provided.

    :rtype: str
    """

    remove_dot = options.get('remove_dot', True)
    lowercase = options.get('lowercase', True)
    name, extension = os.path.splitext(file)

    if remove_dot is not False:
        extension = extension.replace('.', '')

    if lowercase is not False:
        extension = extension.lower()

    return extension


def get_file_name(file, **options):
    """
    gets the file name of given file path.

    :param str file: full file path.

    :keyword bool include_extension: specifies that file extension must be included.
                                     defaults to True if not provided.

    :rtype: str
    """

    include_extension = options.get('include_extension', True)
    root, name = split_name(file)

    if include_extension is False:
        extension = get_file_extension(file, remove_dot=False, lowercase=False)
        return name.rstrip(extension)

    return name


def copy_file(source, target):
    """
    copies the given source file into given target file or directory.

    note that target could also be a directory, if so,
    then the file with the source name will be generated.

    :param str source: source file absolute path.
    :param str target: target file or directory absolute path.
    """

    shutil.copy2(source, target)


def rename_file(source, name):
    """
    rename the given source file

    :param str source: source file absolute path.
    :param str name: new file name.
    """

    root, _ = split_name(source)
    extension = get_file_extension(source, remove_dot=False, lowercase=False)
    new_name = '{name}{extension}'.format(name=name, extension=extension)
    target = os.path.join(root, new_name)
    os.rename(source, target)


def mask_phone_number(phone_number, **options):
    """
    mask phone number.

    :param str phone_number: phone number.

    :rtype: str
    """

    if phone_number in (None, '') or len(phone_number) != 11:
        return phone_number

    return phone_number[0:4] + (len(phone_number) - 6) * '*' + phone_number[-2:]


def generate_filename(filename):
    """
    generate file name.

    :param str filename: file name.

    :rtype: str
    """

    extension = get_file_extension(filename, remove_dot=False)
    filename = datetime.datetime.now().isoformat() + extension

    return filename


def get_standard_mobile_number(mobile):
    """
    gets the standard version of given mobile number.

    for example:

    09383434567 -> 989383434567
    09123433256 -> 989123433256

    if provided mobile number is invalid, it returns None.

    :param str mobile: mobile number.

    :rtype: str
    """

    if not is_valid_mobile(mobile):
        return None

    return f'98{mobile[1:]}'


def get_absolute_url(route):
    """
    gets the absolute url for given url route.

    :param str route: url route.

    :rtype: str
    """

    sep = ''
    if not route.startswith('/'):
        sep = '/'

    return f'{settings.BASE_URL}{sep}{route}'


def get_separated_string(value, group, sep='-'):
    """
    gets the string separated with given character at each provided group length.

    it returns None if the input value is None.

    :param str value: value to be separated.
    :param int group: separate string in groups of this length.
    :param str sep: separator. defaults to '-' if not provided.

    :rtype: str
    """

    if value is None:
        return value

    value = str(value)
    return sep.join(value[i:i + group] for i in range(0, len(value), group))


def verify_recaptcha(g_token: str) -> bool:
    data = {
        'response': g_token,
        'secret': settings.RE_CAPTCHA_SECRET_KEY
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()
    return result_json.get('success') is True
