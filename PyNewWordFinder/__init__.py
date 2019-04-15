# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 11:19
# @Author  : Mr.Robot
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm

from __future__ import unicode_literals
import datetime as dt
import logging
import os
import sys


from . import pynewwordfinder

__version__ = '0.0.1'

is_python3 = sys.version_info[0] > 2
if is_python3:
    unicode = str
logger = logging.getLogger('PyNewWordFinder')

#: The encoding configured by :func:`open`.
ENCODING = 'utf_8'

#: The encoding error handling scheme configured by :func:`open`.
ENCODING_ERRORS = 'strict'


class LicenseError(Exception):
    """A custom exception for missing/invalid license errors."""
    pass


def nwf_init(data_dir=pynewwordfinder.PACKAGE_DIR, encoding=ENCODING,
            encoding_errors=ENCODING_ERRORS, license_code=None):
    if license_code is None:
        license_code = ''
    global ENCODING
    if encoding.lower() in ('utf_8', 'utf-8', 'u8', 'utf', 'utf8'):
        ENCODING = 'utf_8'
        encoding_constant = pynewwordfinder.UTF8_CODE
    elif encoding.lower() in ('gbk', '936', 'cp936', 'ms936'):
        ENCODING = 'gbk'
        encoding_constant = pynewwordfinder.GBK_CODE
    elif encoding.lower() in ('big5', 'big5-tw', 'csbig5'):
        ENCODING = 'big5'
        encoding_constant = pynewwordfinder.BIG5_CODE
    else:
        raise ValueError("encoding must be one of 'utf_8', 'big5', or 'gbk'.")
    logger.debug("Initializing the PyNewWordFinder API: 'data_dir': '{}', 'encoding': "
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

    if not pynewwordfinder.NWF_Init(data_dir, encoding_constant, license_code):
        _attempt_to_raise_license_error(data_dir)
        raise RuntimeError("PyNewWordFinder function 'NWF_Init' failed.")
    else:
        logger.debug("PyNewWordFinder API initialized.")


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
                                           'expired. Try running "PyNewWordFinder '
                                           'update".')
                    elif 'Can not open License file' in line:
                        raise LicenseError('Your license appears to be '
                                           'missing. Try running "PyNewWordFinder '
                                           'update".')


def get_new_words(s, max_key_limit=50, weight_out=True):
    s = _encode(s)
    result = pynewwordfinder.NWF_GetNewWords(s, max_key_limit, weight_out)
    result = _decode(result)
    return result


def get_file_new_words(s, max_key_limit=50, weight_out=True):
    s = _encode(s)
    result = pynewwordfinder.NWF_GetFileNewWords(s, max_key_limit, weight_out)
    result = _decode(result)
    return result


def result_to_user_dict():
    return pynewwordfinder.NWF_Result2UserDict()


def batch_start(file_name):
    return pynewwordfinder.NWF_Batch_Start(_encode(file_name))


def batch_add_mem(s):
    return pynewwordfinder.NWF_Batch_AddMem(_encode(s))


def batch_complete():
    return pynewwordfinder.NWF_Batch_Complete()


def batch_get_result(weight_out=True):
    result = pynewwordfinder.NWF_Batch_GetResult(weight_out)
    return _decode(result)


def batch_add_file():
    return pynewwordfinder.NWF_Batch_AddFile()



def nwf_exit():
    return pynewwordfinder.NWF_Init()


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
