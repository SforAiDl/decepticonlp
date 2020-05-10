import numpy as np
import random

# character level perturbations.
def insert_space(word, ignore=True):
    """
    Insert space at a random position in the word

    word="Somesh"
    edited_word=insert_space(word)
    print(edited_word)
    S omesh

    :param 
    :word: word to be edited
    :ignore: default (True), boolean if assertions should be ignored

    -returns edited word a random space in between
    """
    if ignore and (" " in word or len(word) < 2):
        return word

    assert " " not in word, "given string is not a word"

    assert (
        len(word) >= 2
    ), "Word needs to have a minimum length of 2 for a swap operation"

    index = random.randint(1, len(word) - 1)  # select random index
    return word[:index] + " " + word[index:]  # insert space


def swap(word, ignore=True):
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
    
    :word: word to be edited
    :ignore: default (True), boolean if assertions should be ignored

    -returns word with random character swaps
    """
    if ignore and (" " in word or len(word) < 4):
        return word

    assert " " not in word, "given string is not a word"

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


def delete(word, ignore=True):
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
    if ignore and (" " in word or len(word) < 3):
        return word

    assert " " not in word, "given string is not a word"

    assert (
        len(word) >= 3
    ), "Word needs to have a minimum length of 3 characters for a delete operation"
    index = random.randint(1, len(word) - 2)  # select random index
    return word[:index] + word[index + 1 :]  # delete index


def visual_similar_chars(word, *arg, ignore=True):
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
    if ignore and " " in word:
        return word
    assert " " not in word, "given string is not a word"

    unicode_array = np.array(
        [u"\u0301", u"\u0310", u"\u0305", u"\u0315", u"\u0312", u"\u0302"]
    )

    char_array = np.array(list(word))

    int_pick = np.random.randint(0, high=unicode_array.shape[0], size=len(word))

    picked_unicode = unicode_array[int_pick]

    perturbed_array = np.char.add(char_array, picked_unicode)
    return "".join(perturbed_array)


def midShuffle(word):
    '''
    shuffles the characters of a word, barring the initial and last character
    
    
    word = "Adversarial"
    print(midShuffle('Adversarial'))
    Aaidsvrreal
    
    :param word : word to be shuffled
    
    returns shuffled word with first and last character intact
    
    '''
    if len(word) <= 3:
        return word

    # Split word into first & last letter, and middle letters
    first, mid, last = word[0], word[1:-1], word[-1]
    
    mid = list(mid)
    random.shuffle(mid)

    return first + ''.join(mid) + last


if __name__ == "__main__":
    print(visual_similar_chars("adversarial"))
