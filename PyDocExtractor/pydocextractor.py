# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 11:31
# @Author  : Mr.Robot
# @Site    : 
# @File    : pydocextractor.py
# @Software: PyCharm

from ctypes import (c_bool, c_char, c_char_p, c_double, c_int, c_uint,
                    c_ulong, c_void_p, cdll, POINTER, Structure)
import os
import sys
import logging


is_python3 = sys.version_info[0] > 2
logger = logging.getLogger('doc_extractor_nlpir_py.deLog')

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))

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
    """Loads the NLPIR library appropriate for the user's system.

    This function is called automatically when this module is loaded.

    :param str platform: The platform identifier for the user's system.
    :param bool is_64bit: Whether or not the user's system is 64-bit.
    :param str lib_dir: The directory that contains the library files
        (defaults to :data:`LIB_DIR`).
    :raises RuntimeError: The user's platform is not supported by NLPIR.

    """
    logger.debug("Loading docExtractor library file from '{}'".format(lib_dir))
    if platform.startswith('win') and is_64bit:
        lib = os.path.join(lib_dir, 'win64', 'DocExtractor.dll')
        logger.debug("Using library file for 64-bit Windows.")
    elif platform.startswith('win'):
        lib = os.path.join(lib_dir, 'win32', 'DocExtractor.dll')
        logger.debug("Using library file for 32-bit Windows.")
    elif platform.startswith('linux') and is_64bit:
        lib = os.path.join(lib_dir, 'linux64', 'libDocExtractor.so')
        logger.debug("Using library file for 64-bit GNU/Linux.")
    elif platform.startswith('linux'):
        lib = os.path.join(lib_dir, 'linux32', 'libDocExtractor.so')
        logger.debug("Using library file for 32-bit GNU/Linux.")
    elif platform == 'darwin':
        lib = os.path.join(lib_dir, 'ios', 'libDocExtractor.so')
        logger.debug("Using library file for OSX/iOS.")
    else:
        raise RuntimeError("Platform '{}' is not supported by NLPIR.".format(
                           platform))
    doc_extractor = cdll.LoadLibrary(lib if is_python3 else lib.encode('utf-8'))
    logger.debug("DocExtractor library file '{}' loaded.".format(lib))
    return doc_extractor


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


# Get the exported DocExtractor API functions.
Init = get_func('DE_Init', [c_char_p, c_int, c_char_p], c_int)
"""
int DE_Init(const char *sPath=0,int nEncoding=GBK_CODE,const char *sLicenseCode=0);
初始化
返回：1 - 成功；0 - 失败
备注：在进程中此函数必须在其他函数之前调用（只需执行一次）
参数：  sPath	    - Data文件夹的路径，为空字符串时默认从工程根目录下开始寻找
        nEncoding   - 编码格式，具体如下：
                    0：GBK；1：UTF8；2：BIG5；3：GBK（里面包含繁体字）
        sLicenseCode - 授权码,写成空字符串就可以
"""
DEParserDocE = get_func('DE_ParseDocE', [c_char_p, c_char_p, c_bool, c_uint], c_void_p)
"""
DOC_PARSER_HANDE DE_ParseDocE(const char *sText, const char *sUserDefPos, bool  bSummaryNeeded, unsigned int nFuncRequired)
功能：处理文档，生成handle值，用于后续的文档处理操作
备注：在进程中此函数可以执行多次
参数：
"""
DEGetResult = get_func('DE_GetResult', [c_void_p, c_int], c_char_p)
"""
功能：获得抽取结果
备注：在进程中此函数可以执行多次
参数：
"""
DEGetSentimentScore = get_func('DE_GetSentimentScore', [c_void_p], c_int)
"""
功能：获得情感值
返回：情感值
参数：Handle - DE_ParseDocE获得的值
"""
DEReleaseHandle = get_func('DE_ReleaseHandle', [c_void_p], None)
"""
功能：释放handle
备注：文档抽取结束后应调用该方法，释放handle
参数：Handle - DE_ParseDocE获得的值
"""

DEImportSentimentDict = get_func('DE_ImportSentimentDict', [c_char_p], c_uint)
"""
unsigned int DE_ImportSentimentDict(const char *sFilename)
"""

DEImportUserDict = get_func('DE_ImportUserDict', [c_char_p, c_bool], c_uint)
"""
unsigned int DE_ImportUserDict(const char *sFilename,bool bOverwite=true)
"""

DEImportKeyBlackList = get_func('DE_ImportKeyBlackList', [c_char_p], c_uint)
"""
unsigned int DE_ImportKeyBlackList(const char *sFilename)
"""

DEComputeSentimentDoc = get_func('DE_ComputeSentimentDoc', [c_char_p], c_int)
"""
int  DE_ComputeSentimentDoc(const char *sText)
"""

DEGetLastErrMsg = get_func('DE_GetLastErrMsg', None, c_char_p)
"""
const char* DE_GetLastErrMsg()
"""

DEExit = get_func('DE_Exit', None, None)


if __name__ == "__main__":
    Init
