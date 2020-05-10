import numpy as np
import random
import math

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


def typo(word, probability):
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

    # convert word to list (string is immutable)
    word = list(word)

    num_chars_to_shift = math.ceil(len(word) * probability)

    # checking for capitalizations
    capitalization = [False] * len(word)

    # convert to lowercase and record capitalization
    for i in range(len(word)):
        capitalization[i] = word[i].isupper()
        word[i] = word[i].lower()

    # list of characters to be switched
    positions_to_shift = []
    for i in range(num_chars_to_shift):
        positions_to_shift.append(random.randint(0, len(word) - 1))

    # defining a dictionary of keys located close to each character
    keys_in_proximity = {
        "a": ["q", "w", "s", "x", "z"],
        "b": ["v", "g", "h", "n"],
        "c": ["x", "d", "f", "v"],
        "d": ["s", "e", "r", "f", "c", "x"],
        "e": ["w", "s", "d", "r"],
        "f": ["d", "r", "t", "g", "v", "c"],
        "g": ["f", "t", "y", "h", "b", "v"],
        "h": ["g", "y", "u", "j", "n", "b"],
        "i": ["u", "j", "k", "o"],
        "j": ["h", "u", "i", "k", "n", "m"],
        "k": ["j", "i", "o", "l", "m"],
        "l": ["k", "o", "p"],
        "m": ["n", "j", "k", "l"],
        "n": ["b", "h", "j", "m"],
        "o": ["i", "k", "l", "p"],
        "p": ["o", "l"],
        "q": ["w", "a", "s"],
        "r": ["e", "d", "f", "t"],
        "s": ["w", "e", "d", "x", "z", "a"],
        "t": ["r", "f", "g", "y"],
        "u": ["y", "h", "j", "i"],
        "v": ["c", "f", "g", "v", "b"],
        "w": ["q", "a", "s", "e"],
        "x": ["z", "s", "d", "c"],
        "y": ["t", "g", "h", "u"],
        "z": ["a", "s", "x"],
    }

    # insert typo
    for pos in positions_to_shift:
        # no typo insertion for special characters
        try:
            typo_list = keys_in_proximity[word[pos]]
            word[pos] = random.choice(typo_list)
        except:
            break

    # reinsert capitalization
    for i in range(len(word)):
        if capitalization[i]:
            word[i] = word[i].upper()

    # recombine
    word = "".join(word)

    return word


if __name__ == "__main__":
    print(visual_similar_chars("adversarial"))
