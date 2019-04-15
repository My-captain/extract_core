# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 18:50
# @Author  : Mr.Robot
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm

from __future__ import unicode_literals
import datetime as dt
import logging
import os
import sys

from . import pykeyextractor

__version__ = '0.0.1'

is_python3 = sys.version_info[0] > 2
if is_python3:
    unicode = str
logger = logging.getLogger('PyKeyExtractor')

#: The encoding configured by :func:`open`.
ENCODING = 'utf_8'

#: The encoding error handling scheme configured by :func:`open`.
ENCODING_ERRORS = 'strict'


class LicenseError(Exception):
    """A custom exception for missing/invalid license errors."""
    pass


def ke_init(data_dir=pykeyextractor.PACKAGE_DIR, encoding=ENCODING,
            encoding_errors=ENCODING_ERRORS, license_code=None):
    if license_code is None:
        license_code = ''
    global ENCODING
    if encoding.lower() in ('utf_8', 'utf-8', 'u8', 'utf', 'utf8'):
        ENCODING = 'utf_8'
        encoding_constant = pykeyextractor.UTF8_CODE
    elif encoding.lower() in ('gbk', '936', 'cp936', 'ms936'):
        ENCODING = 'gbk'
        encoding_constant = pykeyextractor.GBK_CODE
    elif encoding.lower() in ('big5', 'big5-tw', 'csbig5'):
        ENCODING = 'big5'
        encoding_constant = pykeyextractor.BIG5_CODE
    else:
        raise ValueError("encoding must be one of 'utf_8', 'big5', or 'gbk'.")
    logger.debug("Initializing the PyKeyExtractor API: 'data_dir': '{}', 'encoding': "
                 "'{}', 'license_code': '{}'".format(
                     data_dir, encoding, license_code))

    global ENCODING_ERRORS
    if encoding_errors not in ('strict', 'ignore', 'replace'):
        raise ValueError("encoding_errors must be one of 'strict', 'ignore', "
                         "or 'replace'.")
    else:
        ENCODING_ERRORS = encoding_errors

    # Init in Python 3 expects bytes, not strings.
    if is_python3 and isinstance(data_dir, str):
        data_dir = _encode(data_dir)
    if is_python3 and isinstance(license_code, str):
        license_code = _encode(license_code)

    if not pykeyextractor.KE_Init(data_dir, encoding_constant, license_code):
        _attempt_to_raise_license_error(data_dir)
        raise RuntimeError("PyKeyExtractor function 'KE_Init' failed.")
    else:
        logger.debug("PyKeyExtractor API initialized.")


def _attempt_to_raise_license_error(data_dir):
    if isinstance(data_dir, bytes):
        data_dir = _decode(data_dir)
    data_dir = os.path.join(data_dir, 'Data')

    current_date = dt.date.today().strftime('%Y%m%d')
    timestamp = dt.datetime.today().strftime('[%Y-%m-%d %H:%M:%S]')
    data_files = os.listdir(data_dir)

    for f in data_files:
        if f == (current_date + '.err'):
            file_name = os.path.join(data_dir, f)
            with open(file_name) as error_file:
                for line in error_file:
                    if not line.startswith(timestamp):
                        continue
                    if 'Not valid license' in line:
                        raise LicenseError('Your license appears to have '
                                           'expired. Try running "PyKeyExtractor '
                                           'update".')
                    elif 'Can not open License file' in line:
                        raise LicenseError('Your license appears to be '
                                           'missing. Try running "PyKeyExtractor '
                                           'update".')


def get_key_words(s, max_key_limit=50, weight_out_needed=True):
    s = _encode(s)
    key_words = pykeyextractor.KE_GetKeyWords(s, max_key_limit, weight_out_needed)
    return _decode(key_words)


def get_file_key_words(s, max_key_limit=50, weight_out_needed=True):
    s = _encode(s)
    key_words = pykeyextractor.KE_GetFileKeyWords(s, max_key_limit, weight_out_needed)
    return _decode(key_words)


def ke_exit():
    is_success = pykeyextractor.KE_Exit()
    return is_success


def _decode(s, encoding=None, errors=None):
    """Decodes *s*."""
    if encoding is None:
        encoding = ENCODING
    if errors is None:
        errors = ENCODING_ERRORS
    return s if isinstance(s, unicode) else s.decode(encoding, errors)


def _encode(s, encoding=None, errors=None):
    """Encodes *s*."""
    if encoding is None:
        encoding = ENCODING
    if errors is None:
        errors = ENCODING_ERRORS
    return s.encode(encoding, errors) if isinstance(s, unicode) else s