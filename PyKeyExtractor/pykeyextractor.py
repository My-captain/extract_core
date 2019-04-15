# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 18:51
# @Author  : Mr.Robot
# @Site    : 
# @File    : pykeyextractor.py
# @Software: PyCharm
from __future__ import unicode_literals
from ctypes import (c_bool, c_char, c_char_p, c_double, c_int, c_uint,
                    c_ulong, c_void_p, cdll, POINTER, Structure)
import logging
import os
import sys

is_python3 = sys.version_info[0] > 2
logger = logging.getLogger('PyKeyExtractor.pykeyextractor')

#: The absolute path to this package (used by NLPIR to find its ``Data``
#: directory). This is a string in Python 2 and a bytes object in Python 3
#: (so it can be used with the :func:`Init` function below).
PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))

#: The absolute path to this path's lib directory.
LIB_DIR = os.path.join(PACKAGE_DIR, 'lib')

"""
nEncoding - 编码格式，具体如下：
0：GBK；1：UTF8；2：BIG5；3：GBK（里面包含繁体字）
"""
#: NLPIR's GBK encoding constant.
GBK_CODE = 0
#: NLPIR's UTF-8 encoding constant.
UTF8_CODE = 1
#: NLPIR's BIG5 encoding constant.
BIG5_CODE = 2
#: NLPIR's GBK (Traditional Chinese) encoding constant.
GBK_FANTI_CODE = 3


def load_library(platform, is_64bit, lib_dir=LIB_DIR):
    logger.debug("Loading docExtractor library file from '{}'".format(lib_dir))
    if platform.startswith('win') and is_64bit:
        lib = os.path.join(lib_dir, 'win64', 'KeyExtract.dll')
        logger.debug("Using library file for 64-bit Windows.")
    elif platform.startswith('win'):
        lib = os.path.join(lib_dir, 'win32', 'KeyExtract.dll')
        logger.debug("Using library file for 32-bit Windows.")
    elif platform.startswith('linux') and is_64bit:
        lib = os.path.join(lib_dir, 'linux64', 'libKeyExtract.so')
        logger.debug("Using library file for 64-bit GNU/Linux.")
    elif platform.startswith('linux'):
        lib = os.path.join(lib_dir, 'linux32', 'libKeyExtract.so')
        logger.debug("Using library file for 32-bit GNU/Linux.")
    else:
        raise RuntimeError("Platform '{}' is not supported by KeyExtractor.".format(
            platform))
    key_extractor = cdll.LoadLibrary(lib if is_python3 else lib.encode('utf-8'))
    logger.debug("KeyExtractor library file '{}' loaded.".format(lib))
    return key_extractor


is_64bit = sys.maxsize > 2**32

libDE = load_library(sys.platform, is_64bit)


def get_func(name, argtypes=None, restype=c_int, lib=libDE):
    """Retrieves the corresponding NLPIR function.

    :param str name: The name of the NLPIR function to get.
    :param list argtypes: A list of :mod:`ctypes` data types that correspond
        to the function's argument types.
    :param restype: A :mod:`ctypes` data type that corresponds to the
        function's return type (only needed if the return type isn't
        :class:`ctypes.c_int`).
    :param lib: A :class:`ctypes.CDLL` instance for the NLPIR API library where
        the function will be retrieved from (defaults to :data:`libNLPIR`).
    :returns: The exported function. It can be called like any other Python
        callable.

    """
    logger.debug("Getting DocExtractor API function: 'name': '{}', 'argtypes': '{}',"
                 " 'restype': '{}'.".format(name, argtypes, restype))
    func = getattr(lib, name)
    if argtypes is not None:
        func.argtypes = argtypes
    if restype is not c_int:
        func.restype = restype
    logger.debug("NLPIR API function '{}' retrieved.".format(name))
    return func


KE_Init = get_func('KeyExtract_Init', [c_char_p, c_int, c_char_p], c_bool)
"""
bool KeyExtract_Init(const char * sDataPath=0,int encode=GBK_CODE,const char*sLicenceCode=0);
功能：为关键词程序准备必要的数据环境；
sDataPath：字典路径；
Encode：编码格式；
sLicenceCode：授权码；
"""

KE_GetKeyWords = get_func('KeyExtract_GetKeyWords', [c_char_p, c_int, c_bool], c_char_p)
"""
const char * KeyExtract_GetKeyWords(const char *sLine,int nMaxKeyLimit=50,bool bWeightOut=false);
功能：从字符串中分析关键词，成功返回true，失败返回false；
sLine：待处理文本头指针；
nMaxKeyLimit：关键词最大数目，最大不超过50，默认为50；
bWeightOut：关键词的输出权重，默认为0；
"""

KE_GetFileKeyWords = get_func('KeyExtract_GetFileKeyWords', [c_char_p, c_int, c_bool], c_char_p)
"""
const char * KeyExtract_GetFileKeyWords(const char *sFilename,int nMaxKeyLimit=50,bool bWeightOut=false);
功能：从文本中分析关键词，成功返回true，失败返回false；
sLine：待处理文本头指针；
nMaxKeyLimit：关键词最大数目，最大不超过50，默认为50；
bWeightOut：关键词的输出权重，默认为0
"""

KE_Exit = get_func('KeyExtract_Exit', None, c_bool)
"""
bool KeyExtract_Exit();
功能：退出，释放资源；进程结束前须调用它释放所占用的内存资源
"""
