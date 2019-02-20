"""
Dummy
"""

import struct
from pybinson.binson_value import BinsonValue
from pybinson.binson_exception import BinsonException


class BinsonInteger(BinsonValue):
    """
    Dummy
    """

    UNPACK_VALUES = {
        0x10: '<b',
        0x11: '<h',
        0x12: '<i',
        0x13: '<q'
    }

    SIZE_IDENTIFIERS = {
        1: 0x10,
        2: 0x11,
        4: 0x12,
        8: 0x13
    }

    @staticmethod
    def instances():
        return int

    @staticmethod
    def identifiers():
        return [0x10, 0x11, 0x12, 0x13]

    @staticmethod
    def int_size(int_val):
        """
        :param int_val:
        :return:
        """
        if -2**7 <= int_val < 2**7:
            return 1
        if -2**15 <= int_val < 2**15:
            return 2
        if -2**31 <= int_val < 2**31:
            return 4
        if -2**63 <= int_val < 2**63:
            return 8
        raise BinsonException('Integer too large to fit in 8 bytes.')

    @staticmethod
    def from_bytes_with_identifier(bytes_rep, offset, forced_identifier):
        """
        :param bytes_rep:
        :param offset:
        :param forced_identifier:
        :return:
        """
        identifier = forced_identifier
        storage_size = (1 << (identifier & 0x0F))
        required_size = 1 + storage_size
        if not required_size + offset <= len(bytes_rep):
            raise BinsonException('Byte array too small to hold integer.')
        unpack = BinsonInteger.UNPACK_VALUES[identifier]
        int_val, = struct.unpack_from(unpack,
                                      bytes_rep,
                                      offset + 1)
        expected_size = BinsonInteger.int_size(int_val)
        if not expected_size == storage_size:
            error_msg = 'Expected storage size {}'.format(expected_size)
            error_msg += ' but got storage size {}.'.format(storage_size)
            raise BinsonException(error_msg)
        return BinsonInteger(int_val), required_size

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        return BinsonInteger.from_bytes_with_identifier(
            bytes_rep, offset, bytes_rep[offset])

    def serialize(self):
        value = self.value
        size = BinsonInteger.int_size(value)
        identifier = BinsonInteger.SIZE_IDENTIFIERS[size]
        pack_val = BinsonInteger.UNPACK_VALUES[identifier]
        raw_bytes = bytearray(1 + (1 << (identifier & 0x0F)))
        raw_bytes[0] = identifier
        struct.pack_into(pack_val, raw_bytes, 1, value)
        return raw_bytes
