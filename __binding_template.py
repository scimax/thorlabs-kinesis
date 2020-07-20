# This script is not meant to be used as standalone. It only acts as a template for 
# generating the bindings found in `thorlabs_kinesis`

from ctypes import Structure, cdll, c_bool, c_short, c_int, c_uint,\
    c_int16, c_int32, c_char, c_byte, c_long, c_float, c_double, \
    POINTER,CFUNCTYPE

from thorlabs_kinesis._utils import c_word, c_dword, bind

lib = cdll.LoadLibrary("__DLL_PATH_PLACEHOLDER__")

