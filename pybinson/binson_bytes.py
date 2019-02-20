"""
Dummy
"""

from pybinson.binson_value import BinsonValue
from pybinson.binson_integer import BinsonInteger
from pybinson.binson_exception import BinsonException


def from_bytes_with_identifier(bytes_rep, offset, forced_identifier):
    """
    :param bytes_rep:
    :param offset:
    :param forced_identifier:
    :return:
    """
    identifier = forced_identifier
    # First we have the length of the byte representation
    forced_identifier = identifier - 0x08
    length, consumed = BinsonInteger.from_bytes_with_identifier(
        bytes_rep, offset, forced_identifier)
    length = length.get_value()
    if not length >= 0:
        error_msg = 'A byte array cannot have negative length'
        raise BinsonException(error_msg)
    required_size = consumed + length
    if not required_size + offset <= len(bytes_rep):
        error_msg = 'Buffer too small for specified length'
        raise BinsonException(error_msg)
    bytes_val = bytes_rep[offset+consumed:offset+consumed+length]
    return bytes_val, required_size


def to_bytes(value):
    """
    :param value:
    :return:
    """
    bytes_rep = BinsonInteger(len(value)).serialize()
    bytes_rep[0] += 0x08
    bytes_rep += value
    return bytes_rep


class BinsonBytes(BinsonValue):
    """
    Dummy
    """

    IDENTIFIERS = [0x18, 0x19, 0x1a]
    INSTANCE_TYPES = (bytearray)

    @staticmethod
    def instances():
        return BinsonBytes.INSTANCE_TYPES

    @staticmethod
    def identifiers():
        return BinsonBytes.IDENTIFIERS

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        bytes_val, consumed = from_bytes_with_identifier(
            bytes_rep, offset, bytes_rep[offset])
        return BinsonBytes(bytes_val), consumed

    def serialize(self):
        return to_bytes(self.value)
