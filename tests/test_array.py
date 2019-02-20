import unittest

from pybinson.binson import BinsonException
from pybinson.binson_array import BinsonArray


class TestBinsonArray(unittest.TestCase):

    def test_sanity(self):
        bytes_rep = bytearray(b'\x42\x44\x45\x43')
        array_val, consumed = BinsonArray.from_bytes(bytes_rep, 0)
        self.assertEqual(consumed, 4)
        bytes_rep2 = BinsonArray(array_val.get_value()).serialize()
        self.assertEqual(bytes_rep, bytes_rep2)
        self.assertEqual(consumed, len(bytes_rep2))
        a = BinsonArray([1,2,3])
        b = BinsonArray()
        b.append(1)
        b.append(2)
        b.append(3)
        self.assertEqual(a.serialize(), b.serialize())
        self.assertRaises(BinsonException, BinsonArray, 1)

    def test_no_end_array(self):
        bytes_rep = bytearray(b'\x42\x44\x45')
        self.assertRaises(BinsonException, BinsonArray.from_bytes, bytes_rep, 0)

    def test_bad_data_type(self):
        array = BinsonArray()
        self.assertRaises(BinsonException, array.append, (1,2,3,4))

if __name__ == '__main__':
        unittest.main()