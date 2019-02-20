"""
Dummy
"""
import six
from pybinson.binson_bytes import from_bytes_with_identifier, to_bytes
from pybinson.binson_value import BinsonValue
from pybinson.binson_exception import BinsonException


class BinsonString(BinsonValue):
    """
    Dummy
    """

    IDENTIFIERS = [0x14, 0x15, 0x16]
    INSTANCE_TYPES = (six.string_types)

    @staticmethod
    def instances():
        return BinsonString.INSTANCE_TYPES

    @staticmethod
    def identifiers():
        return BinsonString.IDENTIFIERS

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        if not bytes_rep[offset] in BinsonString.IDENTIFIERS:
            error_msg = 'Expected string length identifier'
            error_msg += ' (0x14, 0x15, 0x16)'
            error_msg += ' but got {}'.format(bytes_rep[offset])
            raise BinsonException(error_msg)
        bytes_rep, consumed = from_bytes_with_identifier(
            bytes_rep, offset, bytes_rep[offset] + 0x04)
        str_val = bytes_rep.decode('utf8')
        return BinsonString(str_val), consumed

    def serialize(self):
        bytes_rep = to_bytes(self.value.encode('utf8'))
        bytes_rep[0] -= 0x04
        return bytes_rep
