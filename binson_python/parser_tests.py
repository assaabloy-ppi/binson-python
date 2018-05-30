import unittest

from . import Binson
from . import BinsonException

class TestParser(unittest.TestCase):

	def test_bad_input(self):

		# Empty byte array
		self.assertRaises(BinsonException, Binson().fromBytes, bytearray([]))

		# Length < 2 byte array
		self.assertRaises(BinsonException, Binson().fromBytes, bytearray([0x01]))

		# Bad format of first and last byte
		self.assertRaises(BinsonException, Binson().fromBytes, bytearray([0x01, 0x02]))

		# Bad type string
		self.assertRaises(BinsonException, Binson().fromBytes, 'binson')

		# Bad string length
		rawBytes = bytearray([
			0x40,
			0x14, 0xFF, 0x41,	# A
			0x14, 0x01, 0x43,	# C
			0x41
		])
		self.assertRaises(BinsonException, Binson().fromBytes, rawBytes)

	def test_empty_object(self):
		obj = Binson().fromBytes(bytearray([0x40, 0x41]))
		for key in obj.keys():
			self.assertTrue(False)

		self.assertEqual(Binson().toBytes(), bytearray([0x40, 0x41]))
		self.assertEqual(Binson.fromJSON('{}').toBytes(), bytearray([0x40, 0x41]))

	def test_single_string(self):
		# {A:"B"}
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41,	# A
			0x14, 0x01, 0x42,	# B
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertEqual('B', obj.getString('A'))
		self.assertRaises(BinsonException, Binson().getString, 'a')
		self.assertRaises(BinsonException, Binson().getString, 'B')
		self.assertRaises(BinsonException, Binson().getObject, 'A')
		self.assertRaises(BinsonException, Binson().getBool, 'A')
		self.assertRaises(BinsonException, Binson().getInteger, 'A')
		self.assertRaises(BinsonException, Binson().getArray, 'A')
		self.assertRaises(BinsonException, Binson().getBytes, 'A')
		self.assertRaises(BinsonException, Binson().getFloat, 'A')
		self.assertEqual(obj.toBytes(), rawBytes)

		self.assertEqual(Binson().put('A', 'B').toBytes(), rawBytes)
		self.assertEqual(Binson.fromJSON('{"A":"B"}').toBytes(), rawBytes)

		# {A:"C"}
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41,	# A
			0x14, 0x01, 0x43,	# C
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertEqual('C', obj.getString('A'))
		self.assertEqual(obj.toBytes(), rawBytes)
		self.assertEqual(Binson().put('A', 'C').toBytes(), rawBytes)
		self.assertEqual(Binson.fromJSON('{"A":"C"}').toBytes(), rawBytes)

		# {name:"val"}
		rawBytes = bytearray([
			0x40,
			0x14, 0x04, 0x6e, 0x61, 0x6d, 0x65, 	# name
			0x14, 0x03, 0x76, 0x61, 0x6c,			# val
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertEqual('val', obj.getString('name'))
		self.assertEqual(obj.toBytes(), rawBytes)
		b = Binson().put('name', 'val')
		self.assertEqual(b.toBytes(), rawBytes)
		self.assertEqual(Binson.fromJSON('{"name":"val"}').toBytes(), rawBytes)

	def test_multiple_strings(self):

		# {A:"C", B:"D"}
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41,	# A
			0x14, 0x01, 0x43,	# C
			0x14, 0x01, 0x42,	# B
			0x14, 0x01, 0x44,	# D
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertEqual('C', obj.getString('A'))
		self.assertEqual('D', obj.getString('B'))
		self.assertEqual(obj.toBytes(), rawBytes)
		b = Binson().put('A', 'C').put('B', 'D')
		self.assertEqual(b.toBytes(), rawBytes)
		self.assertEqual(Binson.fromJSON('{"A":"C","B":"D"}').toBytes(), rawBytes)

	def test_duplicate(self):

		# {A:"B", A:"C"}
		badBinson = bytearray([
			0x40, 0x14, 0x01, 0x41, 0x14, 0x01, 0x42, 0x14, 0x01, 0x41, 0x14, 0x01, 0x43, 0x41
		])
		self.assertRaises(BinsonException, Binson().fromBytes, badBinson)

	def test_not_sorted(self):
		# {A:"B", A:"C"}
		badBinson = bytearray([
			0x40, 0x14, 0x01, 0x42, 0x14, 0x01, 0x42, 0x14, 0x01, 0x41, 0x14, 0x01, 0x43, 0x41
		])
		self.assertRaises(BinsonException, Binson().fromBytes, badBinson)

	def test_nested_object(self):
		# {A:{A:"B"}}
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41,	# A
				0x40,
				0x14, 0x01, 0x41,	# A
				0x14, 0x01, 0x42,	# B
				0x41,
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertRaises(BinsonException, obj.getString, 'A')
		self.assertEqual('B', obj.getObject('A').getString('A'))
		self.assertEqual(obj.toBytes(), rawBytes)
		b = Binson().put('A', Binson().put('A', 'B'))
		self.assertEqual(b.toBytes(), rawBytes)
		self.assertEqual(Binson.fromJSON('{"A":{"A":"B"}}').toBytes(), rawBytes)

		rawBytes = bytearray([
			0x40,
				0x14, 0x01, 0x41,	# A
				0x40,
					0x14, 0x01, 0x41,	# A
					0x40,
						0x14, 0x01, 0x41,	# A
						0x14, 0x01, 0x42,	# B
					0x41,
				0x41,
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertRaises(BinsonException, obj.getString, 'A')
		self.assertEqual('B', obj.getObject('A').getObject('A').getString('A'))
		self.assertEqual(obj.toBytes(), rawBytes)
		b = Binson().put('A', Binson().put('A', Binson().put('A', 'B')))
		self.assertEqual(b.toBytes(), rawBytes)
		self.assertEqual(Binson.fromJSON('{"A":{"A":{"A":"B"}}}').toBytes(), rawBytes)

		obj = Binson.fromJSON('''
			{
			"country abbreviation": "US",
			"places": [
			    {
			        "place name": "Belmont",
			        "longitude": -71.4594,
			        "post code": "02178",
			        "latitude": 42.4464
			    },
			    {
			        "place name": "Belmont",
			        "longitude": 71.2044,
			        "post code": "02478",
			        "latitude": -42.4128
			    }
			],
			"country": "United States",
			"place name": "Belmont",
			"state": "Massachusetts",
			"state abbreviation": "MA"
			}
		''')
		self.assertEqual('US', obj.getString('country abbreviation'))
		self.assertTrue(isinstance(obj.getArray('places'), list))
		self.assertTrue(isinstance(obj.getArray('places')[0], Binson))
		self.assertEqual('Belmont', obj.getArray("places")[0].getString('place name'))
		self.assertEqual(-71.4594, obj.getArray("places")[0].getFloat('longitude'))
		self.assertEqual('02178', obj.getArray("places")[0].getString('post code'))
		self.assertEqual(42.4464, obj.getArray("places")[0].getFloat('latitude'))
		self.assertTrue(isinstance(obj.getArray('places')[1], Binson))
		self.assertEqual('Belmont', obj.getArray("places")[1].getString('place name'))
		self.assertEqual(71.2044, obj.getArray("places")[1].getFloat('longitude'))
		self.assertEqual('02478', obj.getArray("places")[1].getString('post code'))
		self.assertEqual(-42.4128, obj.getArray("places")[1].getFloat('latitude'))
		self.assertEqual('United States', obj.getString('country'))
		self.assertEqual('Belmont', obj.getString('place name'))
		self.assertEqual('Massachusetts', obj.getString('state'))
		self.assertEqual('MA', obj.getString('state abbreviation'))


	def test_bool(self):
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41,	# A
			0x44,				# True
			0x14, 0x01, 0x42,	# B
			0x45,				# False
			0x41
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertEqual(True, obj.getBool('A'))
		self.assertEqual(False, obj.getBool('B'))
		self.assertEqual(obj.toBytes(), rawBytes)
		b = Binson().put('A', True).put('B', False)
		self.assertEqual(b.toBytes(), rawBytes)

	def test_integer8(self):
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41, 0x10, 0x80,	# "A": -128
			0x14, 0x01, 0x42, 0x10, 0x00,	# "B": 0
			0x14, 0x01, 0x43, 0x10, 0x01,	# "C": 1
			0x14, 0x01, 0x44, 0x10, 0x7F,	# "D": 127
			0x41
		])
		obj = Binson().fromBytes(rawBytes)

		self.assertEqual(-2**7, obj.getInteger('A'))
		self.assertEqual(0, obj.getInteger('B'))
		self.assertEqual(1, obj.getInteger('C'))
		self.assertEqual(2**7 - 1, obj.getInteger('D'))
		self.assertEqual(obj.toBytes(), rawBytes)
		b = Binson()
		b.put('A', -128)
		b.put('B', 0)
		b.put('C', 1)
		b.put('D', 127)
		self.assertEqual(b.toBytes(), rawBytes)


	def test_integer16(self):
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41, 0x11, 0x00, 0x80,	# "A": -2^15 - 1
			0x14, 0x01, 0x42, 0x11, 0x7F, 0xFF,	# "B": -129
			0x14, 0x01, 0x43, 0x11, 0x80, 0x00,	# "C": 128
			0x14, 0x01, 0x44, 0x11, 0xFF, 0x7F,	# "D": 2^15 - 1
			0x41
		])
		obj = Binson().fromBytes(rawBytes)

		self.assertEqual(-2**15, obj.getInteger('A'))
		self.assertEqual(-(2**7 + 1), obj.getInteger('B'))
		self.assertEqual(128, obj.getInteger('C'))
		self.assertEqual(2**15 - 1, obj.getInteger('D'))
		self.assertEqual(obj.toBytes(), rawBytes)

		badLengthInteger = bytearray([
			0x40,
			0x14, 0x01, 0x41, 0x11, 0x7F, 0x00,	# "A": 127
			0x41
		])

		obj = Binson().fromBytes(rawBytes)
		self.assertRaises(BinsonException, Binson().fromBytes, badLengthInteger)

	def test_integer32(self):
		rawBytes = bytearray([
			0x40,
			0x14, 0x01, 0x41, 0x12, 0x00, 0x00, 0x00, 0x80,	# "A": -2^15 - 1
			0x14, 0x01, 0x42, 0x12, 0xFF, 0x7F, 0xFF, 0xFF,	# "B": -2^15 - 2
			0x14, 0x01, 0x43, 0x12, 0x00, 0x80, 0x00, 0x00,	# "C": 2^15
			0x14, 0x01, 0x44, 0x12, 0xFF, 0xFF, 0xFF, 0x7F,	# "D": 2^31 - 1
			0x41
		])
		obj = Binson().fromBytes(rawBytes)

		self.assertEqual(-2**31, obj.getInteger('A'))
		self.assertEqual(-(2**15 + 1), obj.getInteger('B'))
		self.assertEqual(2**15, obj.getInteger('C'))
		self.assertEqual(2**31 - 1, obj.getInteger('D'))
		self.assertEqual(obj.toBytes(), rawBytes)

	def test_dummy(self):
		rawBytes = bytearray([
			0x40, 0x14, 0x01, 0x63, 0x14, 0x05, 0x6c, 0x6f,
			0x67, 0x69, 0x6e, 0x14, 0x01, 0x69, 0x10, 0x0a,
			0x14, 0x01, 0x6f, 0x14, 0x01, 0x73, 0x14, 0x01,
			0x7a, 0x40, 0x14, 0x01, 0x41, 0x14, 0x02, 0x76,
			0x31, 0x14, 0x02, 0x63, 0x68, 0x42, 0x19, 0xbb,
			0x00, 0x5f, 0xc0, 0xd0, 0xe4, 0x76, 0xaa, 0xf6,
			0xe6, 0x2a, 0x8b, 0x89, 0xad, 0x53, 0xf7, 0x28,
			0xaa, 0x29, 0xaa, 0x81, 0x0c, 0xbf, 0x35, 0x6c,
			0xc1, 0x9e, 0x37, 0xaa, 0x02, 0x7c, 0x33, 0x54,
			0x94, 0x93, 0x39, 0x85, 0x8b, 0x36, 0xb7, 0x6d,
			0x1b, 0x06, 0x29, 0x3e, 0x4f, 0x9a, 0x3b, 0x19,
			0x53, 0xa7, 0xee, 0x58, 0x67, 0xaf, 0x2c, 0x04,
			0x5b, 0x02, 0xff, 0x58, 0xdf, 0x45, 0x6a, 0xed,
			0x05, 0x40, 0x14, 0x01, 0x61, 0x18, 0x01, 0x00,
			0x14, 0x02, 0x66, 0x72, 0x18, 0x20, 0x55, 0x29,
			0xce, 0x8c, 0xcf, 0x68, 0xc0, 0xb8, 0xac, 0x19,
			0xd4, 0x37, 0xab, 0x0f, 0x5b, 0x32, 0x72, 0x37,
			0x82, 0x60, 0x8e, 0x93, 0xc6, 0x26, 0x4f, 0x18,
			0x4b, 0xa1, 0x52, 0xc2, 0x35, 0x7b, 0x14, 0x01,
			0x70, 0x42, 0x18, 0x01, 0x0b, 0x14, 0x02, 0x6c,
			0x75, 0x43, 0x14, 0x02, 0x74, 0x63, 0x18, 0x0c,
			0x50, 0x01, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff,
			0xff, 0x7f, 0x00, 0x00, 0x14, 0x02, 0x74, 0x6e,
			0x14, 0x03, 0x42, 0x6f, 0x62, 0x14, 0x02, 0x74,
			0x6f, 0x18, 0x20, 0x07, 0xe2, 0x8d, 0x4e, 0xe3,
			0x2b, 0xfd, 0xc4, 0xb0, 0x7d, 0x41, 0xc9, 0x21,
			0x93, 0xc0, 0xc2, 0x5e, 0xe6, 0xb3, 0x09, 0x4c,
			0x62, 0x96, 0xf3, 0x73, 0x41, 0x3b, 0x37, 0x3d,
			0x36, 0x16, 0x8b, 0x41, 0x43, 0x41, 0x41,
		])
		obj = Binson().fromBytes(rawBytes)
		self.assertEqual('login', obj.getString('c'))
		self.assertEqual(10, obj.getInteger('i'))
		self.assertEqual('s', obj.getString('o'))
		zObj = obj.getObject('z')
		self.assertEqual('v1', zObj.getString('A'))
		ch = zObj.getArray('ch')
		self.assertTrue(isinstance(ch[0], bytearray))
		self.assertEqual(obj.toBytes(), rawBytes)

		rawBytes = bytearray([
			0x40, 0x14, 0x01, 0x61, 0x18, 0x01, 0x00,
			0x14, 0x02, 0x66, 0x72, 0x18, 0x20, 0x55, 0x29,
			0xce, 0x8c, 0xcf, 0x68, 0xc0, 0xb8, 0xac, 0x19,
			0xd4, 0x37, 0xab, 0x0f, 0x5b, 0x32, 0x72, 0x37,
			0x82, 0x60, 0x8e, 0x93, 0xc6, 0x26, 0x4f, 0x18,
			0x4b, 0xa1, 0x52, 0xc2, 0x35, 0x7b, 0x14, 0x01,
			0x70, 0x42, 0x18, 0x01, 0x0b, 0x14, 0x02, 0x6c,
			0x75, 0x43, 0x14, 0x02, 0x74, 0x63, 0x18, 0x0c,
			0x50, 0x01, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff,
			0xff, 0x7f, 0x00, 0x00, 0x14, 0x02, 0x74, 0x6e,
			0x14, 0x03, 0x42, 0x6f, 0x62, 0x14, 0x02, 0x74,
			0x6f, 0x18, 0x20, 0x07, 0xe2, 0x8d, 0x4e, 0xe3,
			0x2b, 0xfd, 0xc4, 0xb0, 0x7d, 0x41, 0xc9, 0x21,
			0x93, 0xc0, 0xc2, 0x5e, 0xe6, 0xb3, 0x09, 0x4c,
			0x62, 0x96, 0xf3, 0x73, 0x41, 0x3b, 0x37, 0x3d,
			0x36, 0x16, 0x8b, 0x41
		])
		obj = Binson().fromBytes(rawBytes)
			

if __name__ == '__main__':
	unittest.main()