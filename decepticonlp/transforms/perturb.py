import numpy as np
import random

# character level perturbations.
def insert_space(word):
    """
    Insert space at a random position in the word

    word="Somesh"
    edited_word=insert_space(word)
    print(edited_word)
    S omesh

    :param word - word to be edited

    -returns edited word a random space in between
    """

    index = random.randint(0, len(word))  # select random index
    return word[:index] + " " + word[index:]  # insert space


def swap(word):
    """
    Swaps two adjacent characters in a word which are not at the either end
    Implies that the word is at least four characters long

    word=input()

    #If input's length is less than 4
    swap(word)      #Input Hey
    Assertion Error

    #If input's length is greater than or equal to 4
    swap(word)      #Input WHAT
    WAHT
    
    :param word - word to be edited

    -returns word with random character swaps
    """

    assert (
        len(word) >= 4
    ), "Word needs to have a minimum length of 4 characters for a swap operation"
    charlist = list(word)
    index = random.randint(1, len(word) - 3)  # select random offset for tuple
    charlist[index], charlist[index + 1] = (
        charlist[index + 1],
        charlist[index],
    )  # swap tuple
    return "".join(charlist)


def delete(word):
    """
    Deletes a random character which is not at the either end
    Implies that the word is at least three characters long

    word=input()

    #If input's length is less than 3
    swap(word)      #Input He
    Assertion Error

    #If input's lenght is greater than or equal to 3
    swap(word)      #Input Hey
    Hy
    
    :param word - word to be edited

    -returns word with random character deletion
    """
    assert (
        len(word) >= 3
    ), "Word needs to have a minimum length of 3 characters for a delete operation"
    index = random.randint(1, len(word) - 2)  # select random index
    return word[:index] + word[index + 1 :]  # delete index


def visual_similar_chars(word, *arg):

    method_pick = np.random.randint(0, len(arg))
    if arg[method_pick] == "unicode":
        """
        get diacritic  characters
        """
        char_array = np.array(list(word))
        diacritic = np.char.add(char_array, u"\u0301")
        return diacritic
    if arg[method_pick] == "visual":
        """
        get visually similar chars. like @ for a. 0 for O.
        """
        return None


print(visual_similar_chars("shashank", "unicode", "visual"))
