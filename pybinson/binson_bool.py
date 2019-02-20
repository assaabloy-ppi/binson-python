"""
Dummy
"""

from pybinson.binson_value import BinsonValue


class BinsonBool(BinsonValue):
    """
    Dummy
    """

    IDENTIFIERS = [0x44, 0x45]
    INSTANCE_TYPES = (bool)

    @staticmethod
    def instances():
        return BinsonBool.INSTANCE_TYPES

    @staticmethod
    def identifiers():
        return BinsonBool.IDENTIFIERS

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        bool_val = bytes_rep[offset] == 0x44
        return BinsonBool(bool_val), 1

    def serialize(self):
        if self.value is True:
            return bytearray(b'\x44')
        return bytearray(b'\x45')
