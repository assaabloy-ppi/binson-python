"""
Dummy
"""

import struct
from pybinson.binson_value import BinsonValue
from pybinson.binson_exception import BinsonException


class BinsonFloat(BinsonValue):
    """
    Dummy
    """

    IDENTIFIERS = [0x46]
    INSTANCE_TYPES = (float)

    @staticmethod
    def instances():
        return BinsonFloat.INSTANCE_TYPES

    @staticmethod
    def identifiers():
        return BinsonFloat.IDENTIFIERS

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        required_size = 1 + 8
        if not required_size + offset <= len(bytes_rep):
            error_msg = 'Byte array too small to hold a float'
            raise BinsonException(error_msg)
        float_val, = struct.unpack_from('<d', bytes_rep, offset + 1)
        return BinsonFloat(float_val), 9

    def serialize(self):
        bytes_rep = bytearray(9)
        bytes_rep[0] = 0x46
        struct.pack_into('<d', bytes_rep, 1, self.value)
        return bytes_rep
