import unittest

from pybinson.binson_float import BinsonFloat

class TestBinsonFloat(unittest.TestCase):

    def test_sanity(self):
        bytes_rep = BinsonFloat(-71.4594).serialize()
        float_rep, consumed = BinsonFloat.from_bytes(bytes_rep, 0)
        self.assertEqual(consumed, 9)
        self.assertEqual(-71.4594, float_rep.get_value())


if __name__ == '__main__':
        unittest.main()