import abc
import math
import random
import json
import string
import numpy as np
from pathlib import Path


class CharacterPerturbations(metaclass=abc.ABCMeta):
    """
        An abstract class used to represent the character perturbations.SubClass should implement the apply method.
        Methods
        -------
        apply(self, word: str, **kwargs)
            - applies the perturbation on the word and returns it.
    """

    @abc.abstractmethod
    def apply(self, word: str, **kwargs):
        """Applies perturbation and returns the word."""
        raise NotImplementedError

    def get_ignore_default_value(self):
        return True

    def get_string_not_a_word_error_msg(self):
        return "given string is not a word"


class InsertSpaceCharacterPerturbations(CharacterPerturbations):
    """
        A class used to apply space character perturbations.
        Methods
        -------
        apply(self, word: str, **kwargs)
            - applies the space perturbation on the word and returns it.
    """

    def apply(self, word: str, char_perturb=False, **kwargs):
        """
            Insert space or character at a random position in the word

            word="Somesh"
            edited_word=insert_space(word)
            print(edited_word)
            S omesh

            word="Hello"
            edited_word=insert_space(word,char_perturb=True)
            print(edited_word)
            Henllo

            :param
            :word: word to be edited
            :char_perturb: default(False), boolean, adds a character instead of spaces
            :ignore: default (True), boolean if assertions should be ignored
            -returns edited word a random space in between
            """

        if kwargs.get("ignore", self.get_ignore_default_value()) and (
            " " in word or len(word) < 2
        ):
            return word

        assert " " not in word, self.get_string_not_a_word_error_msg()

        assert (
            len(word) >= 2
        ), "Word needs to have a minimum length of 2 for an insert operation"

        if char_perturb == True:
            index = random.randint(0, len(word))  # select random index
            return (
                word[:index] + random.choice(string.ascii_letters[:26]) + word[index:]
            )  # insert character
        else:
            index = random.randint(1, len(word) - 1)  # select random index
            return word[:index] + " " + word[index:]  # insert space


class ShuffleCharacterPerturbations(CharacterPerturbations):
    """
        A class used to apply shuffle character perturbations.
        Methods
        -------
        apply(self, word: str, **kwargs)
            - applies the shuffle perturbation on the word and returns it.
    """

    def apply(self, word: str, **kwargs):
        """
            if mid=True:
            shuffles the characters of a word at random, barring the initial and last character
            else:
            swaps any two characters of a word at random, barring the initial and last character


            word = "Adversarial"
            print(shuffle('Adversarial',mid=True))
            Aaidsvrreal

            word = "WHAT"
            print(shuffle('WHAT',mid=False))
            WAHT

            :param word : word to be shuffled
            :param mid :
            if set, it shuffle all the characters barring the initial and last
            if not set, it swap any two characters barring the initial and last


            returns shuffled word with first and last character intact

            """
        if kwargs.get("ignore", self.get_ignore_default_value()) and (
            " " in word or len(word) < 4
        ):
            return word

        assert " " not in word, self.get_string_not_a_word_error_msg()

        assert (
            len(word) >= 4
        ), "Word needs to have a minimum length of 4 for a shuffle operation"

        if kwargs.get("mid", True):
            # Split word into first & last letter, and middle letters
            first, mid, last = word[0], word[1:-1], word[-1]

            mid = list(mid)
            random.shuffle(mid)

            return first + "".join(mid) + last
        else:
            char_list = list(word)
            index = random.randint(1, len(word) - 3)  # select random offset for tuple
            char_list[index], char_list[index + 1] = (
                char_list[index + 1],
                char_list[index],
            )  # swap tuple
            return "".join(char_list)


class DeleteCharacterPerturbations(CharacterPerturbations):
    """
        A class used to apply delete character perturbations.
        Methods
        -------
        apply(self, word: str, **kwargs)
            - applies the delete perturbation on the word and returns it.
    """

    def apply(self, word: str, **kwargs):
        """
                Deletes a random character which is not at the either end
                Implies that the word is at least three characters long

                word=input()

                #If input's length is less than 3
                delete(word)      #Input He
                Assertion Error

                #If input's lenght is greater than or equal to 3
                delete(word)      #Input Hey
                Hy

                :word: word to be edited
                :ignore: default (True), boolean if assertions should be ignored

                -returns word with random character deletion
                """
        if kwargs.get("ignore", self.get_ignore_default_value()) and (
            " " in word or len(word) < 3
        ):
            return word

        assert " " not in word, self.get_string_not_a_word_error_msg()

        assert (
            len(word) >= 3
        ), "Word needs to have a minimum length of 3 characters for a delete operation"
        index = random.randint(1, len(word) - 2)  # select random index
        return word[:index] + word[index + 1 :]  # delete index


class TypoCharacterPerturbations(CharacterPerturbations):
    """
        A class used to apply typo character perturbations.
        Methods
        -------
        apply(self, word: str, **kwargs)
            - applies the typo perturbation on the word and returns it.
    """

    def apply(self, word: str, **kwargs):
        """
            shifts a character by one keyboard space:
            one space up, down, left or right
            each word is typofied with some probability 'p':
            1. (p*100) percent of character will become typos
            keyboard is defined as:
            qwertyuiop
            asdfghjkl
             zxcvbnm
            word = "Noise"
            print(typo('Noise',0.1))
            Noide
            :param word : word to be shuffled
            :param probability: probability of a typo
            returns typofied word
            """

        if kwargs.get("ignore", self.get_ignore_default_value()) and (" " in word):
            return word

        assert " " not in word, self.get_string_not_a_word_error_msg()

        word = list(word)
        chars = len(word)
        num_chars_to_shift = math.ceil(chars * kwargs.get("probability", 0.1))

        # list of characters to be switched
        positions_to_shift = random.sample(range(chars), num_chars_to_shift)

        # defining a dictionary of keys located close to each character
        json_path = Path("decepticonlp/transforms/keys_in_proximity.json")
        keys_in_proximity = json.load(open(json_path, "r"))

        for i, c in enumerate(word):
            # Check Upper

            # Check if in position and given keys
            if i in positions_to_shift and c in keys_in_proximity:
                word[i] = random.choice(keys_in_proximity[c])

        # recombine
        word = "".join(word)
        return word


class VisuallySimilarCharacterPerturbations(CharacterPerturbations):
    """
        A class used to apply visually similar character perturbations.
        Methods
        -------
        apply(self, word: str, **kwargs)
            - applies the visually similar perturbation on the word and returns it.
    """

    def apply(self, word: str, **kwargs):
        np.random.seed(0)
        """
            unicode_array is a list of different unicodes.
            each char of the word is perturbed by a unicode chosen at random
            from the unicode_array.

            :word: word to be edited
            :ignore: default (True), boolean if assertions should be ignored

            eg:
            input : adversarial
            output : a̐d̅v̕e̒ŕŝa̅r̕îál̂

            visual_similar_chars("Hey Stop")
            Hey Stop

            visual_similar_chars("Hey Stop", ignore=False)
            assertion error
            """
        if kwargs.get("ignore", self.get_ignore_default_value()) and " " in word:
            return word
        assert " " not in word, self.get_string_not_a_word_error_msg()

        unicode_array = np.array(
            [u"\u0301", u"\u0310", u"\u0305", u"\u0315", u"\u0312", u"\u0302"]
        )

        char_array = np.array(list(word))

        int_pick = np.random.randint(0, high=unicode_array.shape[0], size=len(word))

        picked_unicode = unicode_array[int_pick]

        perturbed_array = np.char.add(char_array, picked_unicode)
        return "".join(perturbed_array)

    def apply_homoglyph(self, word: str, **kwargs):
        """ 
        input : adversarial
        output : @d𑣀𝓮𝓻ꮪ𝕒г𝜾а1
        Applies homoglyph to each char in word.
        If char is not present in dictionary,
        same char is returned.
        Check dictionary.py for code to get homoglyph char.
        """

        if kwargs.get("ignore", self.get_ignore_default_value()) and " " in word:
            return word
        assert " " not in word, self.get_string_not_a_word_error_msg()

        json_path = Path("homoglyph.json")
        homoglyph_dic = json.load(open(json_path, "r"))

        char_list = list(word)

        char_list_glyph = []
        for char in char_list:
            glyph_string = homoglyph_dic[char]
            glyph_pick = np.random.choice(len(glyph_string), 1)[0]
            char_list_glyph.append(glyph_string[glyph_pick])

        return "".join(char_list_glyph)    
if __name__ == "__main__":
    viz=VisuallySimilarCharacterPerturbations()
    print(viz.apply('adversarial'))