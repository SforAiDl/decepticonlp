import abc
import random


class Preprocessing(metaclass=abc.ABCMeta):
    """
        An abstract class used to preprocess textual data from the user. Subclasses implement the apply method.
        Methods
        -------
        apply(self, text1: str, **kwargs)
            - applies the respective filter and return the new string.
    """

    @abc.abstractmethod
    def apply(self, text1: str, **kwargs):  # pragma: no cover
        """applies filter and returns new string"""
        raise NotImplementedError

    def get_ignore_default_value(self):
        return True
