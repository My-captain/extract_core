# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 12:47
# @Author  : Mr.Robot
# @Site    :
# @File    : __init__.py
# @Software: PyCharm

from __future__ import unicode_literals
import datetime as dt
import logging
import os
import sys


from . import pydocextractor

__version__ = '0.0.1'

is_python3 = sys.version_info[0] > 2
if is_python3:
    unicode = str
logger = logging.getLogger('PyDocExtractor')

#: The encoding configured by :func:`open`.
ENCODING = 'utf_8'

#: The encoding error handling scheme configured by :func:`open`.
ENCODING_ERRORS = 'strict'


class LicenseError(Exception):
    """A custom exception for missing/invalid license errors."""
    pass


def de_init(data_dir=pydocextractor.PACKAGE_DIR, encoding=ENCODING,
            encoding_errors=ENCODING_ERRORS, license_code=None):
    if license_code is None:
        license_code = ''
    global ENCODING
    if encoding.lower() in ('utf_8', 'utf-8', 'u8', 'utf', 'utf8'):
        ENCODING = 'utf_8'
        encoding_constant = pydocextractor.UTF8_CODE
    elif encoding.lower() in ('gbk', '936', 'cp936', 'ms936'):
        ENCODING = 'gbk'
        encoding_constant = pydocextractor.GBK_CODE
    elif encoding.lower() in ('big5', 'big5-tw', 'csbig5'):
        ENCODING = 'big5'
        encoding_constant = pydocextractor.BIG5_CODE
    else:
        raise ValueError("encoding must be one of 'utf_8', 'big5', or 'gbk'.")
    logger.debug("Initializing the NLPIR API: 'data_dir': '{}', 'encoding': "
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

    if not pydocextractor.Init(data_dir, encoding_constant, license_code):
        _attempt_to_raise_license_error(data_dir)
        raise RuntimeError("DocExtractor function 'DE_Init' failed.")
    else:
        logger.debug("DocExtractor API initialized.")


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
                                           'expired. Try running "PyDocExtractor '
                                           'update".')
                    elif 'Can not open License file' in line:
                        raise LicenseError('Your license appears to be '
                                           'missing. Try running "PyDocExtractor '
                                           'update".')


def doc_extract(s, s_user_def_pos=None, is_summary_needed=True, n_func_required=0xffff):
    s = _encode(s)
    doc_parser_handle = pydocextractor.DEParserDocE(s, s_user_def_pos, is_summary_needed, n_func_required)
    result = []
    for i in range(13):
        res_i = _decode(pydocextractor.DEGetResult(doc_parser_handle, i))
        result.append(res_i)
    sentiment_score = pydocextractor.DEGetSentimentScore(doc_parser_handle)
    return result, sentiment_score


def import_user_dict(file_path, is_overwrite=True):
    pydocextractor.DEImportUserDict(_encode(file_path), is_overwrite)


def import_sentiment_dict(file_path):
    pydocextractor.DEImportSentimentDict(_encode(file_path))


def import_key_black_list(file_path):
    pydocextractor.DEImportKeyBlackList(_encode(file_path))


def compute_sentiment_doc(text):
    s = _encode(text)
    sentiment_score = pydocextractor.DEComputeSentimentDoc(s)
    return sentiment_score


def get_last_error_msg():
    return _decode(pydocextractor.DEGetLastErrMsg())


def release_handle(doc_parser_handle):
    pydocextractor.DEReleaseHandle(doc_parser_handle)


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
