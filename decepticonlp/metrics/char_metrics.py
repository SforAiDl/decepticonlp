import abc
import math
import random
import string
import numpy as np
from pathlib import Path


class CharacterMetrics(metaclass=abc.ABCMeta):
    """
        An abstract class used to represent the character metrics. Subclasses implement the calculate method.
        Methods
        -------
        apply(self, text1: str, text2: str, **kwargs)
            - calculates the similarity/distance between two strings using the appropriate metric.
    """

    @abc.abstractmethod
    def calculate(self, text1: str, text2: str, **kwargs):  # pragma: no cover
        """calculates distance/similarity and returns the same"""
        raise NotImplementedError

    def get_ignore_default_value(self):
        return True


class Levenshtein(CharacterMetrics):
    """
        A class used to calculate the levenshtein distance between two strings.
        Methods
        
        -------
        calculate(self, text1:str, text2: str, **kwargs)
            - calculates levenshtein distance and returns the same
    """

    def calculate(self, text1: str, text2: str, normalize="none", **kwargs):
        """
        Calculate Levenshtein Distance using dynamic programming optimized with (np)
        DP - O(m*n) complexity - Recursive approach - O(3^m)

        Example:
        from perturb import levenshtein
        print(levenshtein("Hey","HEY"))
        2.0

        #Normalize Levenshtein Distance - Total strategy
        print(levenshtein("Hey", "HEY", normalize="sum"))
        0.33333

        #Normalize LCS - Max Strategy
        print(levenshtein("HeyS", "HEY", normalize="lcs"))
        0.75


        :params
        :text1 : First string to be compared
        :text2 : Second string to be compared
        :normalize: pass "sum" for total Levenshtein distance, "lcs" for maximum normalization, "none" default
        :type text1: String
        :type text2: String
        :type normalize: String

        returns levenshtein distance
        :return type: float

        IMPORTANT NOTE :
        The normalized distance is not a metric, as it violates the triangle inequality.
        https://stackoverflow.com/questions/45783385/normalizing-the-edit-distance
        """

        size_x, size_y = len(text1) + 1, len(text2) + 1
        matrix = np.zeros((size_x, size_y))
        x, y = np.arange(size_x), np.arange(size_y)
        matrix[x, 0] = x
        matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if text1[x - 1] == text2[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1,
                    )
        distance = matrix[size_x - 1, size_y - 1]
        if normalize == "sum":
            return distance / (size_x + size_y - 2)
        elif normalize == "lcs":
            return distance / (max(size_x, size_y) - 1)
        else:
            return matrix[size_x - 1, size_y - 1]


class Jaccard(CharacterMetrics):
    """
        A class used to calculate the jaccard similarity between two strings.
        Methods
        
        -------
        calculate(self, text1:str, text2: str, **kwargs)
            - calculates jaccard similarity and returns the same
    """

    def calculate(self, text1: str, text2: str, ngrams=1, **kwargs):
        """
        Calculate Jaccard Distance :
        J(X,Y) = |X∩Y| / |X∪Y|
        Jaccard Distance = 1-J(X,Y)

        Example:
        from perturb import jaccard
        print(jaccard("Hey","HEY"))
        0.8

        :text1 : First string to be compared
        :text2 : Second string to be compared
        :ngrams : Select the ngram range
        :ignore : Boolean to ignore assertions
        :type text1: String
        :type text2: String
        :type ngrams: int

        returns jaccard distance
        """

        if kwargs.get("ignore", self.get_ignore_default_value()) and not (
            len(text1) >= ngrams and len(text2) >= ngrams
        ):
            return self.calculate(text1, text2)

        assert (
            len(text1) >= ngrams and len(text2) >= ngrams
        ), "text size lesser than ngrams passed"

        grams1 = [tuple(text1[i : i + ngrams]) for i in range(len(text1) - ngrams + 1)]
        grams2 = [tuple(text2[i : i + ngrams]) for i in range(len(text2) - ngrams + 1)]
        x, y = set(grams1), set(grams2)
        n, d = len(x.intersection(y)), len(x.union(y))
        return 1 - (n / d)


class Euclidean(CharacterMetrics):
    """
        A class used to calculate the Euclidean distance between two strings.
        Methods
        
        -------
        calculate(self, text1:str, text2: str, **kwargs)
            - calculates euclidean distance and returns the same
    """

    def calculate(self, text1: str, text2: str, norm=False, **kwargs):
        """
        the Euclidean distance between strings p and q given,
        the Euclidean space is exactly the word vector space.

        Example:
        from perturb import euclid

        #Norm=False
        print(euclid("Hey","HEY"))
        1.4142135623730951

        print(euclid("Hey there I am mahajan","HEY there I mahajan"))
        1.7320508075688772

        #Norm=True
        print(euclid("Hey","HEY",norm=True))
        1.0

        print(euclid("Hey there I am mahajan","HEY there I mahajan", norm=True))
        0.7071067811865476

        :params
        :text1 : First string to be compared
        :text2 : Second string to be compared
        :normalize: False (default) to return the euclidean distance, True to return standardised (between 0 and 1) euclidean distance
        :type text1: String
        :type text2: String
        :type normalize: Boolean

        returns euclidean distance
        """

        vocab = set(text1.split() + text2.split())
        dic = dict.fromkeys(vocab, 0)
        for word in text1.split(" "):
            dic[word] += 1
        vec_text1 = np.fromiter(dic.values(), dtype=int)
        dic = dict.fromkeys(vocab, 0)
        for word in text2.split(" "):
            dic[word] += 1
        vec_text2 = np.fromiter(dic.values(), dtype=int)
        dist = np.linalg.norm(vec_text1 - vec_text2)

        if norm:
            return dist / np.sqrt(len(vocab))
        else:
            return dist
