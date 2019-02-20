import unittest

from pybinson.binson_string import BinsonString

class TestBinsonString(unittest.TestCase):

    def test_sanity(self):
        bytes_rep = bytearray(b'\x14\x01\x41')
        string_val, consumed = BinsonString.from_bytes(bytes_rep, 0)
        self.assertEqual(1, len(string_val.get_value()))
        self.assertEqual(string_val.get_value()[0], 'A')
        self.assertEqual(consumed, 3)

        bytes_rep2 = BinsonString('A').serialize()
        self.assertEqual(bytes_rep, bytes_rep2)


if __name__ == '__main__':
    unittest.main()