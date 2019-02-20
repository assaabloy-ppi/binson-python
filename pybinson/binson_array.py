"""
Dummy
"""
from pybinson.binson_exception import BinsonException
from pybinson.binson_value import BinsonValue
from pybinson.array_interface import BinsonArrayInterface


class BinsonArray(BinsonValue, BinsonArrayInterface):
    """
    Dummy
    """

    INSTANCE_TYPES = (list)

    @staticmethod
    def instances():
        return BinsonArray.INSTANCE_TYPES

    @staticmethod
    def identifiers():
        return [0x42]

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        from pybinson import binson_values
        orig_offset = offset
        offset += 1
        array = []
        while offset < len(bytes_rep):

            # End array
            if bytes_rep[offset] == 0x43:
                offset += 1
                consumed = offset - orig_offset
                return BinsonArray(array), consumed

            identifier = bytes_rep[offset]
            parser = binson_values.get_parser(identifier)
            binson_value, consumed = parser(bytes_rep, offset)
            array.append(binson_value)
            offset += consumed

        raise BinsonException('Unexpected end of byte array')

    def __init__(self, array=None):
        from pybinson.binson_values import binsonify_value
        if not array:
            array = []
        if not isinstance(array, list):
            error_msg = 'Value of type {}'.format(type(array))
            error_msg += ' cannot be represented as binson.'
            raise BinsonException(error_msg)
        super(BinsonArray, self).__init__(array)
        for i in range(0, len(self.value)):
            self.value[i] = binsonify_value(self.value[i])
        self._set_list(self.value)

    def serialize(self):
        """
        :return:
        """
        bytes_rep = bytearray(b'\x42')
        for value in self.value:
            bytes_rep += value.serialize()
        bytes_rep += bytearray(b'\x43')
        return bytes_rep
