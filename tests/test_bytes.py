import unittest

from pybinson.binson_bytes import BinsonBytes
from pybinson.binson_integer import BinsonInteger


class TestBinsonBytes(unittest.TestCase):

    def test_sanity(self):
        bytes_rep = bytearray(b'\x18\x01\x01')
        bytes_val, consumed = BinsonBytes.from_bytes(bytes_rep, 0)
        self.assertEqual(1, len(bytes_val.get_value()))
        self.assertEqual(bytes_val.get_value()[0], bytes_rep[2])
        self.assertEqual(consumed, 3)

        bytes_rep2 = BinsonBytes(bytearray(b'\x01')).serialize()
        self.assertEqual(bytes_rep, bytes_rep2)
        self.assertTrue(isinstance(bytes_val.get_value(), bytearray))


    def helper(self, length):
        original = bytearray(length)
        bytes_rep = BinsonBytes(original).serialize()
        parsed, consumed = BinsonBytes.from_bytes(bytes_rep, 0)
        self.assertTrue(isinstance(parsed.get_value(), bytearray))
        self.assertEqual(original, parsed.get_value())
        self.assertEqual(consumed, len(original) + 1 + BinsonInteger.int_size(length))

    def test_bytes(self):
        self.helper(0)
        self.helper(1)
        self.helper(127)
        self.helper(128)
        self.helper(2**15-1)
        # More than this takes very long to run :)

if __name__ == '__main__':
        unittest.main()