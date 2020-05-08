import numpy as np
import random
# character level perturbations.
def insert_space(word):
    """
    insert spaces at random places in words to make them 
    look like different words to fool the model.
    Performs a single split and returns a list of two 
    new strings.
    """
    length=len(word)
    split_int=np.random.randint(0,high=length)
    split_list=word.split(word[split_int])

    if len(split_list[0])>len(split_list[1]): # adds word[split_int] to string with lesser length.
        split_list[1]+=word[split_int]
    else:
        split_list[0]+=word[split_int]    

    return split_list
def swap(word):
    """
    swaps random two adjacent letters but keeps 
    intact the first and last letter. Naturally a string
    of size>=4 is required for this.
    """
    chars=list(word)
    i = random.randint(1,len(word)-2)
    chars[i],chars[i+1]=chars[i+1],chars[i]
    return ''.join(chars)

def delete(word):
    """
    Deletes a random character from a word
    except for first and last character.
    """
    word_part=list(word[1:-1])
    length=len(word_part)
    delete_index=np.random.randint(0,high=length)

    word_part.pop(delete_index)

    word_part.append(word[-1])
    word_part=list(word[0])+word_part

    return ''.join(word_part)
def visual_similar_chars(word,*arg):

    method_pick=np.random.randint(0,len(arg))   
    if arg[method_pick]=='unicode': 
        """
        get diacritic  characters
        """ 
        char_array=np.array(list(word))
        diacritic=np.char.add(char_array,u'\u0301')
        return diacritic
    if arg[method_pick]=='visual':
        """
        get visually similar chars. like @ for a. 0 for O.
        """
        return None  
print(visual_similar_chars('shashank','unicode','visual'))   

