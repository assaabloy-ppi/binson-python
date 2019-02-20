"""
Dummy
"""

from pybinson.binson_exception import BinsonException
from pybinson.binson_string import BinsonString
from pybinson.binson_interface import BinsonInterface


class Binson(BinsonInterface):
    """
    Dummy
    """

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        from pybinson.binson_values import get_parser
        if not offset < len(bytes_rep):
            error_msg = 'Byte array too small to hold a binson object.'
            raise BinsonException(error_msg)
        orig_offset = offset
        if not bytes_rep[offset] in Binson.identifiers():
            raise BinsonException('Unexpected start of binson object.')
        offset += 1
        dict_rep = {}
        prev_name = ''
        length = len(bytes_rep)
        while offset < length:

            # End of object
            if bytes_rep[offset] == 0x41:
                offset += 1
                consumed = offset - orig_offset
                return Binson(dict_rep), consumed

            # Parse field name (BinsonString)
            name, consumed = BinsonString.from_bytes(bytes_rep, offset)
            name = name.get_value()
            offset += consumed

            if name <= prev_name:
                error_msg = 'Fields names not in lexicographical order'
                error_msg += ' when parsing. Current: {}'.format(name)
                error_msg += ', previous: {}'.format(prev_name)
                raise BinsonException(error_msg)

            identifier = bytes_rep[offset]
            parser = get_parser(identifier)
            binson_value, consumed = parser(bytes_rep, offset)
            offset += consumed
            dict_rep[name] = binson_value
            prev_name = name

        # We should never end ep here if it is a valid binson object
        raise BinsonException('Unexpected end of byte array')

    @staticmethod
    def identifiers():
        return [0x40]

    @staticmethod
    def instances():
        return dict

    def __init__(self, dict_rep=None):
        from pybinson.binson_values import binsonify_dict
        if not dict_rep:
            dict_rep = {}
        # Convert native types to BinsonValue representation
        binsonify_dict(dict_rep)
        super(Binson, self).__init__(dict_rep)

    def __eq__(self, other):
        if isinstance(other, Binson):
            return self.serialize() == other.serialize()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def serialize(self):
        """
        :return:
        """
        bytes_rep = bytearray(b'\x40')
        for field in sorted(self.value.keys()):
            bytes_rep += BinsonString(field).serialize()
            bytes_rep += self.value[field].serialize()
        bytes_rep += bytearray(b'\x41')
        return bytes_rep
