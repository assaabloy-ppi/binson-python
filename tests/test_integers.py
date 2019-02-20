import unittest

from pybinson.binson_integer import BinsonInteger

class TestBinsonInteger(unittest.TestCase):

    def test_sanity(self):
        bytes_rep = bytearray(b'\x10\x01')
        int_val, consumed = BinsonInteger.from_bytes(bytes_rep, 0)
        self.assertEqual(bytes_rep, BinsonInteger(int_val.get_value()).serialize())

    def test_int_size(self):

        # 1 byte size representation
        self.assertEqual(BinsonInteger.int_size(-2**7), 1)
        self.assertEqual(BinsonInteger.int_size(-2**7 + 1), 1)
        self.assertEqual(BinsonInteger.int_size(-1), 1)
        self.assertEqual(BinsonInteger.int_size(0), 1)
        self.assertEqual(BinsonInteger.int_size(1), 1)
        self.assertEqual(BinsonInteger.int_size(2**7 - 2), 1)
        self.assertEqual(BinsonInteger.int_size(2**7 - 1), 1)

        # 2 bytes size representation
        self.assertEqual(BinsonInteger.int_size(-2**15), 2)
        self.assertEqual(BinsonInteger.int_size(-2**15 + 1), 2)
        self.assertEqual(BinsonInteger.int_size(-2**7 - 1), 2)
        self.assertEqual(BinsonInteger.int_size(2**15 - 2), 2)
        self.assertEqual(BinsonInteger.int_size(2**15 - 1), 2)

        # 4 bytes size representation
        self.assertEqual(BinsonInteger.int_size(-2**31), 4)
        self.assertEqual(BinsonInteger.int_size(-2**31 + 1), 4)
        self.assertEqual(BinsonInteger.int_size(-2**15 - 1), 4)
        self.assertEqual(BinsonInteger.int_size(2**31 - 2), 4)
        self.assertEqual(BinsonInteger.int_size(2**31 - 1), 4)

        # 8 bytes size representation
        self.assertEqual(BinsonInteger.int_size(-2**63), 8)
        self.assertEqual(BinsonInteger.int_size(-2**63 + 1), 8)
        self.assertEqual(BinsonInteger.int_size(-2**31 - 1), 8)
        self.assertEqual(BinsonInteger.int_size(2**63 - 2), 8)
        self.assertEqual(BinsonInteger.int_size(2**63 - 1), 8)

    def test_integers_8(self):

        INTEGERS = [
            -2**7,
            -1,
            0,
            1,
            2**7 - 1,
        ]

        for i in INTEGERS:
            bytes_rep = BinsonInteger(i).serialize()
            int_val, consumed = BinsonInteger.from_bytes(bytes_rep, 0)
            self.assertEqual(i, int_val.get_value())
            self.assertEqual(consumed, 2)

    def test_integers_16(self):

        INTEGERS = [
            -2**15,
            -2**15 + 1,
            -2**7 - 1,
            2**7,
            2**15 - 1
        ]

        for i in INTEGERS:
            bytes_rep = BinsonInteger(i).serialize()
            int_val, consumed = BinsonInteger.from_bytes(bytes_rep, 0)
            self.assertEqual(i, int_val.get_value())
            self.assertEqual(consumed, 3)

    def help_integer_32(self, value):
        bytes_rep = BinsonInteger(value).serialize()
        int_val, consumed = BinsonInteger.from_bytes(bytes_rep, 0)
        self.assertEqual(value, int_val.get_value())
        self.assertEqual(consumed, 5)

    def test_integers_32(self):
        self.help_integer_32(-2**31)
        self.help_integer_32(-2**31 + 1)
        self.help_integer_32(-2**15 - 1)
        self.help_integer_32(2**15)
        self.help_integer_32(2**31 - 1)

    def test_bytes_rep(self):
        BYTE_REPS = [
            b'\x10\x01',
            b'\x11\x01\x01',
            b'\x12\x01\x01\x01\x01',
            b'\x13\x01\x01\x01\x01\x01\x01\x01\x01'
        ]
        for i in BYTE_REPS:
            i = bytearray(i)
            int_val, consumed = BinsonInteger.from_bytes(i, 0)
            bytes_rep = BinsonInteger(int_val.get_value()).serialize()
            self.assertEqual(consumed, len(i))
            self.assertEqual(bytes_rep, i)


if __name__ == '__main__':
        unittest.main()