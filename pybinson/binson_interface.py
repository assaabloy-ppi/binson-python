"""
Dummy
"""
import json

import pybinson
from pybinson.binson_array import BinsonArray
from pybinson.binson_bool import BinsonBool
from pybinson.binson_bytes import BinsonBytes
from pybinson.binson_exception import BinsonException
from pybinson.binson_float import BinsonFloat
from pybinson.binson_integer import BinsonInteger
from pybinson.binson_string import BinsonString
from pybinson.binson_value import BinsonValue


class BinsonInterface(BinsonValue):
    """
    Dummy
    """

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        pass

    @staticmethod
    def identifiers():
        pass

    @staticmethod
    def instances():
        pass

    def serialize(self):
        pass

    @staticmethod
    def deserialize(bytes_rep, offset=0, check_trailing_garbage=True):
        """
        :param bytes_rep:
        :param offset:
        :param check_garbage:
        :return:
        """
        binson, consumed = pybinson.binson.Binson.from_bytes(bytes_rep, offset)
        if check_trailing_garbage:
            if not offset + consumed == len(bytes_rep):
                error_msg = 'Detected garbage after object end.'
                raise BinsonException(error_msg)
        return binson

    def keys(self):
        """
        :return:
        """
        return self.value.keys()

    def put(self, field_name, value):
        """
        :param field_name:
        :param value:
        :return:
        """
        self.value[field_name] = pybinson.binson_values.binsonify_value(value)
        return self

    def __get(self, field, expected_type):
        """
        :param field:
        :param expected_type:
        :return:
        """
        if field not in self.value:
            raise BinsonException(
                'Binson object does not contain field name "%s"' % field)
        value = self.value[field]
        if not isinstance(value, expected_type):
            raise BinsonException(
                'Field name "%s" does not contain expected field' % field)
        if not isinstance(value, (BinsonArray, pybinson.binson.Binson)):
            value = value.get_value()
        return value

    def get_integer(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, BinsonInteger)

    def get_float(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, BinsonFloat)

    def get_string(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, BinsonString)

    def get_bytes(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, BinsonBytes)

    def get_bool(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, BinsonBool)

    def get_array(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, BinsonArray)

    def get_object(self, field_name):
        """
        :param field_name:
        :return:
        """
        return self.__get(field_name, pybinson.binson.Binson)

    def to_json(self, indent=4):
        """
        :param indent:
        :return:
        """
        def jsonify_binson(value):
            """
            :param value:
            :return:
            """
            if isinstance(value, BinsonBytes):
                ret = '0x'
                for i in value.get_value():
                    ret += '%02x' % i
                return ret
            return value.get_value()
        return json.dumps(self.value, default=jsonify_binson, indent=indent)

    @staticmethod
    def from_json(json_str):
        """
        :param json_str:
        :return:
        """
        def binsonify_json(obj):
            """
            :param obj:
            :return:
            """
            import six
            for field in obj:
                value = obj[field]
                if isinstance(value, six.string_types) and len(value) > 4:
                    if value[0:2].upper() == '0X':
                        try:
                            tmp = bytearray.fromhex(value[2:])
                            obj[field] = tmp
                        except ValueError:
                            pass
            return obj
        dict_rep = json.loads(json_str, object_hook=binsonify_json)
        return pybinson.binson.Binson(dict_rep)
