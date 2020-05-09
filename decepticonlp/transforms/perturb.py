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

    #If input's lenght is greater than or equal to 4
    swap(word)      #Input WHAT
    WAHT
    
    :param word - word to be edited

    -returns word with random character swaps
    """

    assert (
        len(word) >= 4
    ), "Word needs to have a minimum length of 4 for a swap operation"
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
    ), "Word needs to have a minimum length of 3 for a delete operation"
    index = random.randint(1, len(word) - 2)  # select random index
    return word[:index] + word[index + 1 :]  # delete index


def visual_similar_chars(word, *arg):
    """
    unicode_array is a list of different unicodes.
    each char of the word is perturbed by a unicode chosen at random
    from the unicode_array.
    
    eg:
    input : adversarial
    output : a̐d̅v̕e̒ŕŝa̅r̕îál̂
    """

    unicode_array = np.array(
        [u"\u0301", u"\u0310", u"\u0305", u"\u0315", u"\u0312", u"\u0302"]
    )

    char_array = np.array(list(word))

    int_pick = np.random.randint(0, high=unicode_array.shape[0], size=len(word))

    picked_unicode = unicode_array[int_pick]

    perturbed_array = np.char.add(char_array, picked_unicode)
    return "".join(perturbed_array)


if __name__ == "__main__":
    print(visual_similar_chars("adversarial"))
