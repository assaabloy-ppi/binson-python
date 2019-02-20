import fuzzing
from pybinson.binson import Binson
from pybinson.binson_exception import BinsonException

seed = bytearray([
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
fuzz_factor = 7


while True:
    fuzzed_data = fuzzing.fuzzer(seed, fuzz_factor)
    try:
        a = Binson.deserialize(fuzzed_data)
    except BinsonException:
        pass
    except UnicodeDecodeError:
        pass


