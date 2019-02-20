"""
Dummy
"""


import pybinson
from pybinson.binson_exception import BinsonException
from pybinson.binson_value import BinsonValue

BINSON_VALUES = [
    pybinson.binson_bool.BinsonBool,
    pybinson.binson_array.BinsonArray,
    pybinson.binson_string.BinsonString,
    pybinson.binson_bytes.BinsonBytes,
    pybinson.binson_float.BinsonFloat,
    pybinson.binson_integer.BinsonInteger,
    pybinson.binson.Binson
]


def get_parser(identifier):
    """
    :param identifier:
    :return:
    """
    ret_parser = None
    for parser in BINSON_VALUES:
        if identifier in parser.identifiers():
            ret_parser = parser.from_bytes
            break
    if not ret_parser:
        error_msg = 'Value 0x%02x' % identifier
        error_msg += ' is not a valid binson identifier.'
        raise BinsonException(error_msg)
    return ret_parser


def binsonify_value(value):
    """
    :param value:
    :return:
    """
    binson_rep = None
    if isinstance(value, BinsonValue):
        binson_rep = value
    else:
        for binson_value in BINSON_VALUES:
            if isinstance(value, binson_value.instances()):
                binson_rep = binson_value(value)
                break
    if not binson_rep:
        error_msg = 'Value of type {}'.format(type(value))
        error_msg += ' cannot be represented as binson.'
        raise BinsonException(error_msg)
    return binson_rep


def binsonify_dict(value):
    """
    :param value:
    :return:
    """
    for field in value.keys():
        value[field] = binsonify_value(value[field])
