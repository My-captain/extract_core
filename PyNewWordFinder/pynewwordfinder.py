# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 11:22
# @Author  : Mr.Robot
# @Site    : 
# @File    : pynewwordfinder.py
# @Software: PyCharm
from __future__ import unicode_literals
from ctypes import (c_bool, c_char, c_char_p, c_double, c_int, c_uint,
                    c_ulong, c_void_p, cdll, POINTER, Structure)
import logging
import os
import sys

is_python3 = sys.version_info[0] > 2
logger = logging.getLogger('PyNewWordFinder.pynewwordfinder')

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
        lib = os.path.join(lib_dir, 'win64', 'NewWordFinder.dll')
        logger.debug("Using library file for 64-bit Windows.")
    elif platform.startswith('win'):
        lib = os.path.join(lib_dir, 'win32', 'NewWordFinder.dll')
        logger.debug("Using library file for 32-bit Windows.")
    elif platform.startswith('linux') and is_64bit:
        lib = os.path.join(lib_dir, 'linux64', 'libNewWordFinder.so')
        logger.debug("Using library file for 64-bit GNU/Linux.")
    elif platform.startswith('linux'):
        lib = os.path.join(lib_dir, 'linux32', 'libNewWordFinder.so')
        logger.debug("Using library file for 32-bit GNU/Linux.")
    else:
        raise RuntimeError("Platform '{}' is not supported by NewWordFinder.".format(
            platform))
    key_extractor = cdll.LoadLibrary(lib if is_python3 else lib.encode('utf-8'))
    logger.debug("NewWordFinder library file '{}' loaded.".format(lib))
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
    logger.debug("Getting NewWordFinder API function: 'name': '{}', 'argtypes': '{}',"
                 " 'restype': '{}'.".format(name, argtypes, restype))
    func = getattr(lib, name)
    if argtypes is not None:
        func.argtypes = argtypes
    if restype is not c_int:
        func.restype = restype
    logger.debug("NewWordFinder API function '{}' retrieved.".format(name))
    return func


NWF_Init = get_func('NWF_Init', [c_char_p, c_int, c_char_p], c_bool)
"""
bool NWF_Init(const char * sInitDirPath=0，int encoding=GBK_CODE,const
char*sLicenceCode=0); 
"""

NWF_Exit = get_func('NWF_Exit', None, c_bool)
"""
bool NWF_Exit(); 
"""

NWF_GetNewWords = get_func('NWF_GetNewWords', [c_char_p, c_int, c_bool], c_char_p)
"""
const char * NWF_GetNewWords(const char *sLine,int nMaxKeyLimit=50,bool
bWeightOut=false);
"""

NWF_GetFileNewWords = get_func('NWF_GetFileNewWords', [c_char_p, c_int, c_bool], c_char_p)
"""
const char * NWF_GetFileNewWords(const char *sTextFile,int
nMaxKeyLimit=50,bool bWeightOut=false);

"""

NWF_Result2UserDict = get_func('NWF_Result2UserDict', None, c_int)
"""
unsigned int NWF_Result2UserDict();
"""

NWF_Batch_Start = get_func('NWF_Batch_Start', None, c_bool)
"""
bool NWF_Batch_Start();
"""

NWF_Batch_AddFile = get_func('NWF_Batch_AddFile', [c_char_p], c_int)
"""
 int NWF_Batch_AddFile(const char *sFilename);
"""

NWF_Batch_AddMem = get_func('NWF_Batch_AddMem', [c_char_p], c_bool)
"""
bool NWF_Batch_AddMem(const char *sText);
"""

NWF_Batch_Complete = get_func('NWF_Batch_Complete', None, c_bool)
"""
bool NWF_Batch_Complete();
"""

NWF_Batch_GetResult = get_func('NWF_Batch_GetResult', [c_bool], c_char_p)
"""
const char * NWF_Batch_GetResult(bool bWeightOut=false)
"""
