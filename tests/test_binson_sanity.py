import unittest

from pybinson.binson_array import BinsonArray
from pybinson.binson import Binson
from pybinson.binson_value import BinsonValue


class TestBinsonSanity(unittest.TestCase):

    def sanity_helper(self, obj, nested=False):
        obj.get_integer('A')
        obj.get_float('B')
        obj.get_string('C')
        obj.get_bool('D')
        obj.get_bytes('E')
        array = obj.get_array('F')
        array.get(0)
        array.get(1)
        array.get(2)
        array = obj.get_array('G')
        array.get(0)
        array.get(1)
        array.get(2)
        obj.get_object('H')
        if not nested:
            self.sanity_helper(obj.get_object('I'), True)
    def test_sanity(self):
        obj = Binson()
        obj.put('A', 1).put('B', 3.14).put('C', 'Hello World!')
        obj.put('D', False).put('E', bytearray(b'\x01\x02'))
        obj.put('F', [1,2,3]).put('G', BinsonArray().append(1).append(2).append(3))
        obj.put('H', {})
        cpy = Binson.deserialize(obj.serialize())
        obj.put('I', cpy)

        obj2 = Binson({
            "A": 1,
            "B": 3.14,
            "C": 'Hello World!',
            "D": False,
            "E": bytearray(b'\x01\x02'),
            "F": [1,2,3],
            "G": BinsonArray([1,2,3]),
            "H": Binson(),
            "I": {
                "A": 1,
                "B": 3.14,
                "C": 'Hello World!',
                "D": False,
                "E": bytearray(b'\x01\x02'),
                "F": [1,2,3],
                "G": BinsonArray([1,2,3]),
                "H": {}
            }
        })

        self.sanity_helper(obj)
        self.sanity_helper(obj2)

        obj3 = Binson.deserialize(obj.serialize())
        obj3.put('I', cpy)
        self.sanity_helper(obj3)
        self.assertTrue(obj == obj2)
        self.assertTrue(obj2 == obj3)
        self.assertFalse(obj2 == 23)
        self.assertTrue(obj2 != 23)
        obj4 = Binson.from_json('''
        {
            "A": 1,
            "B": 3.14,
            "C": "Hello World!",
            "D": false,
            "E": "0x0102",
            "F": [1,2,3],
            "G": [1,2,3],
            "H": {},
            "I": {
                "A": 1,
                "B": 3.14,
                "C": "Hello World!",
                "D": false,
                "E": "0x0102",
                "F": [1,2,3],
                "G": [1,2,3],
                "H": {}
            }
        }
        ''')
        self.assertTrue(obj4 == obj)
        self.sanity_helper(obj4)
        str1 = obj.to_json()
        str2 = obj2.to_json()
        str3 = obj3.to_json()
        str4 = obj4.to_json()
        self.assertEqual(str1, str2)
        self.assertEqual(str2, str3)
        self.assertEqual(str3, str4)

    def test_binson_value(self):
        self.assertRaises(NotImplementedError, BinsonValue.instances)
        self.assertRaises(NotImplementedError, BinsonValue.identifiers)
        self.assertRaises(NotImplementedError, BinsonValue.from_bytes, bytearray(b'\x40'))
        a = BinsonValue(1)
        self.assertRaises(NotImplementedError, a.serialize)

if __name__ == '__main__':
    unittest.main()