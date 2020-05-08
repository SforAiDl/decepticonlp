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
    index=random.randint(0,len(word)) #select random index
    return word[:index]+' '+word[index:] #insert space

def swap(word):
    """
    swaps random two adjacent letters but keeps 
    intact the first and last letter. Naturally a string
    of size>=4 is required for this.
    """
    charlist=list(word)
    index = random.randint(1,len(word)-3) #select random offset for tuple
    charlist[index],charlist[index+1]=charlist[index+1],charlist[index] #swap tuple
    return ''.join(charlist)

def delete(word):
    """
    Deletes a random character from a word
    except for first and last character.
    """
    index=random.randint(1,len(word)-2) #select random index
    return word[:index]+word[index+1:] #delete index

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

