"""
Dummy
"""

from pybinson.binson_value import BinsonValue


class BinsonBool(BinsonValue):
    """
    Dummy
    """

    def serialize(self):
        if self.value is True:
            return bytearray(b'\x44')
        return bytearray(b'\x45')

    @staticmethod
    def instances():
        return bool

    @staticmethod
    def identifiers():
        return [0x44, 0x45]

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        bool_val = bytes_rep[offset] == 0x44
        return BinsonBool(bool_val), 1
