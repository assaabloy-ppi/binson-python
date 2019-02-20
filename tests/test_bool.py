import unittest

from pybinson.binson_bool import BinsonBool

class TestBinsonBool(unittest.TestCase):

    def test_true(self):
        bytes_rep = bytearray(b'\x44')
        bool_val, consumed = BinsonBool.from_bytes(bytes_rep, 0)
        self.assertEqual(True, bool_val.get_value())
        self.assertEqual(consumed, 1)
        bytes_rep2 = BinsonBool(True).serialize()
        self.assertEqual(bytes_rep2, bytes_rep)

    def test_false(self):
        bytes_rep = bytearray(b'\x45')
        bool_val, consumed = BinsonBool.from_bytes(bytes_rep, 0)
        self.assertEqual(False, bool_val.get_value())
        self.assertEqual(consumed, 1)
        bytes_rep2 = BinsonBool(False).serialize()
        self.assertEqual(bytes_rep2, bytes_rep)


if __name__ == '__main__':
    unittest.main()