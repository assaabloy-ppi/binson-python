"""
Dummy
"""


class BinsonValue(object):
    """
    Dummy
    """

    def __init__(self, value):
        self.value = value

    def serialize(self):
        """
        :return:
        """
        raise NotImplementedError()

    def get_value(self):
        """
        :return:
        """
        return self.value

    @staticmethod
    def instances():
        """
        Returns a list of which python instances is represented with
        this type.
        """
        raise NotImplementedError()

    @staticmethod
    def identifiers():
        """
        Returns a list of which bytes identifies the type.
        """
        raise NotImplementedError()

    @staticmethod
    def from_bytes(bytes_rep, offset=0):
        """
        Converts the binson byte representation to value and returns
        the number of bytes consumed. Assumes that offset < len(bytes_rep)
        """
        raise NotImplementedError()
