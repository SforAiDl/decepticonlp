import abc
import random
from nltk.stem import *
from nltk.tokenize import sent_tokenize, word_tokenize


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


class Stem(Preprocessing):
    """
        A class used to stem the words in a string
        -------
        apply(self, text1:str, **kwargs)
            - applies the stem filter and returns the string
        
        NOTE: The PorterStemmer has been used the default here.
        
        Example:
        st = Stem()
        print(st.apply("Dinosaurs were killed by asteroids"))
        dinosaur were kill by asteroid 
        
        print(st.apply("Dinosaurs were killed by asteroids".type="lancaster"))
        dinosa wer kil by asteroid 
        
        :params
        :text1 : String to be stemmed
        :type: The kind of stemmer to be used
        :type text1: String
        :type type: String
        
        ## MORE FUNCTIONALITY NEEDS TO BE ADDED
    """

    def apply(self, text1: str, type="default", **kwargs):
        """
        """
        stemmer = None
        if type == "default":
            stemmer = PorterStemmer()
        elif type == "lancaster":
            stemmer = LancasterStemmer()

        word_tokens = text1.split()
        stem_word_tokens = []
        for word in word_tokens:
            stem_word_tokens.append(stemmer.stem(word))
            stem_word_tokens.append(" ")

        return "".join(stem_word_tokens)
