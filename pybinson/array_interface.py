"""
Dummy
"""
import pybinson
from pybinson.binson_object import BinsonObject
from pybinson.binson_value import BinsonValue


class BinsonArrayInterface(object):
    """
    Dummy
    """

    def __init__(self):
        self.value = None

    def _set_list(self, value):
        """
        :param value:
        :return:
        """
        self.value = value

    def append(self, value):
        """
        :param value:
        :return:
        """
        from pybinson import binson_values
        if not isinstance(value, BinsonValue):
            value = binson_values.binsonify_value(value)
        self.value.append(value)
        return self

    def get(self, index):
        """
        :param index:
        :return:
        """
        assert index < len(self.value)
        ret_val = self.value[index]
        self_instances = (pybinson.binson_array.BinsonArray,
                          BinsonObject)
        if not isinstance(ret_val, self_instances):
            ret_val = ret_val.value
        return ret_val
