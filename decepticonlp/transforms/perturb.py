import numpy as np 
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
    def swap_two_chars(char_list,a,b): # make as decorator later.
        s=''
        s=char_list[a]
        char_list[a]=char_list[b]
        char_list[b]=s
        
    word_part=list(word[1:-1]) # want to deal with all letters except first and last.
    length=len(word_part)
    int_pick=np.random.randint(0,length)
     
   
    if int_pick==0:
        swap_two_chars(word_part,1,0)

    elif int_pick==length-1:
        swap_two_chars(word_part,length-1,length-2)

    else:
        # choose to swap with left of right.
        l_r=np.random.randint(0,high=2)
        if l_r==0:
            swap_two_chars(word_part,int_pick,int_pick-1)
        else:
            swap_two_chars(word_part,int_pick,int_pick+1)

    word_part.append(word[-1])
    word_part=list(word[0])+word_part
    return ''.join(word_part)

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

