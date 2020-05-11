import numpy as np
import random
import math

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


def shuffle(word, mid=True, ignore=True):
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
    if ignore and (" " in word or len(word) < 4):
        return word

    assert " " not in word, "given string is not a word"

    assert (
        len(word) >= 4
    ), "Word needs to have a minimum length of 4 for a shuffle operation"

    if mid:
        # Split word into first & last letter, and middle letters
        first, mid, last = word[0], word[1:-1], word[-1]

        mid = list(mid)
        random.shuffle(mid)

        return first + "".join(mid) + last
    elif mid == False:
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


def typo(word, probability=0.1, ignore=True):
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

    if ignore and (" " in word):
        return word

    assert " " not in word, "given string is not a word"

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


def visual_similar_chars(word, *arg, ignore=True):
    """
    unicode_array is a list of different unicodes.
    each char of the word is perturbed by a unicode chosen at random
    from the unicode_array.
    
    :word: word to be edited
    :ignore: default (True), boolean if assertions should be ignored

    eg:
    If the unicode method is chosen:
    input : adversarial
    output : a̐d̅v̕e̒ŕŝa̅r̕îál̂

    If the homoglyph method is chosen:
    input : adversarial
    output : @d𑣀𝓮𝓻ꮪ𝕒г𝜾а1

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
    d = {
        "a": "@aɑαа⍺ａ𝐚𝑎𝒂𝒶𝓪𝔞𝕒𝖆𝖺𝗮𝘢𝙖𝚊𝛂𝛼𝜶𝝰𝞪",
        "b": "bƄЬᏏᑲᖯｂ𝐛𝑏𝒃𝒷𝓫𝔟𝕓𝖇𝖻𝗯𝘣𝙗𝚋",
        "c": "cϲсᴄⅽⲥꮯｃ𐐽𝐜𝑐𝒄𝒸𝓬𝔠𝕔𝖈𝖼𝗰𝘤𝙘𝚌",
        "d": "dԁᏧᑯⅆⅾꓒｄ𝐝𝑑𝒅𝒹𝓭𝔡𝕕𝖉𝖽𝗱𝘥𝙙𝚍",
        "e": "eеҽ℮ℯⅇꬲｅ𝐞𝑒𝒆𝓮𝔢𝕖𝖊𝖾𝗲𝘦𝙚𝚎",
        "f": "fſϝքẝꞙꬵｆ𝐟𝑓𝒇𝒻𝓯𝔣𝕗𝖋𝖿𝗳𝘧𝙛𝚏𝟋",
        "g": "gƍɡցᶃℊｇ𝐠𝑔𝒈𝓰𝔤𝕘𝖌𝗀𝗴𝘨𝙜𝚐",
        "h": "hһհᏂℎｈ𝐡𝒉𝒽𝓱𝔥𝕙𝖍𝗁𝗵𝘩𝙝𝚑",
        "i": "!iıɩɪ˛ͺιіӏᎥιℹⅈⅰ⍳ꙇꭵｉ𑣃𝐢𝑖𝒊𝒾𝓲𝔦𝕚𝖎𝗂𝗶𝘪𝙞𝚒𝚤𝛊𝜄𝜾𝝸𝞲",
        "j": "jϳјⅉｊ𝐣𝑗𝒋𝒿𝓳𝔧𝕛𝖏𝗃𝗷𝘫𝙟𝚓",
        "k": "kｋ𝐤𝑘𝒌𝓀𝓴𝔨𝕜𝖐𝗄𝗸𝘬𝙠𝚔",
        "l": "1",
        "m": "mｍ",
        "n": "nոռｎ𝐧𝑛𝒏𝓃𝓷𝔫𝕟𝖓𝗇𝗻𝘯𝙣𝚗",
        "o": "0",
        "p": "pρϱр⍴ⲣｐ𝐩𝑝𝒑𝓅𝓹𝔭𝕡𝖕𝗉𝗽𝘱𝙥𝚙𝛒𝛠𝜌𝜚𝝆𝝔𝞀𝞎𝞺𝟈",
        "q": "qԛգզｑ𝐪𝑞𝒒𝓆𝓺𝔮𝕢𝖖𝗊𝗾𝘲𝙦𝚚",
        "r": "rгᴦⲅꭇꭈꮁｒ𝐫𝑟𝒓𝓇𝓻𝔯𝕣𝖗𝗋𝗿𝘳𝙧𝚛",
        "s": "sƽѕꜱꮪｓ𐑈𑣁𝐬𝑠𝒔𝓈𝓼𝔰𝕤𝖘𝗌𝘀𝘴𝙨𝚜",
        "t": "tｔ𝐭𝑡𝒕𝓉𝓽𝔱𝕥𝖙𝗍𝘁𝘵𝙩𝚝",
        "u": "uʋυսᴜꞟꭎꭒｕ𐓶𑣘𝐮𝑢𝒖𝓊𝓾𝔲𝕦𝖚𝗎𝘂𝘶𝙪𝚞𝛖𝜐𝝊𝞄𝞾",
        "v": "vνѵטᴠⅴ∨⋁ꮩｖ𑜆𑣀𝐯𝑣𝒗𝓋𝓿𝔳𝕧𝖛𝗏𝘃𝘷𝙫𝚟𝛎𝜈𝝂𝝼𝞶",
        "w": "wɯѡԝաᴡꮃｗ𑜊𑜎𑜏𝐰𝑤𝒘𝓌𝔀𝔴𝕨𝖜𝗐𝘄𝘸𝙬𝚠",
        "x": "x×хᕁᕽ᙮ⅹ⤫⤬⨯ｘ𝐱𝑥𝒙𝓍𝔁𝔵𝕩𝖝𝗑𝘅𝘹𝙭𝚡",
        "y": "yɣʏγуүყᶌỿℽꭚｙ𑣜𝐲𝑦𝒚𝓎𝔂𝔶𝕪𝖞𝗒𝘆𝘺𝙮𝚢𝛄𝛾𝜸𝝲𝞬",
        "z": "zᴢꮓｚ𑣄𝐳𝑧𝒛𝓏𝔃𝔷𝕫𝖟𝗓𝘇𝘻𝙯𝚣",
        "A": "AΑАᎪᗅᴀꓮꭺＡ𐊠𖽀𝐀𝐴𝑨𝒜𝓐𝔄𝔸𝕬𝖠𝗔𝘈𝘼𝙰𝚨𝛢𝜜𝝖𝞐",
        "B": "BʙΒВвᏴᏼᗷᛒℬꓐꞴＢ𐊂𐊡𐌁𝐁𝐵𝑩𝓑𝔅𝔹𝕭𝖡𝗕𝘉𝘽𝙱𝚩𝛣𝜝𝝗𝞑",
        "C": "CϹСᏟℂℭⅭⲤꓚＣ𐊢𐌂𐐕𐔜𑣩𑣲𝐂𝐶𝑪𝒞𝓒𝕮𝖢𝗖𝘊𝘾𝙲🝌",
        "D": "DᎠᗞᗪᴅⅅⅮꓓꭰＤ𝐃𝐷𝑫𝒟𝓓𝔇𝔻𝕯𝖣𝗗𝘋𝘿𝙳",
        "E": "EΕЕᎬᴇℰ⋿ⴹꓰꭼＥ𐊆𑢦𑢮𝐄𝐸𝑬𝓔𝔈𝔼𝕰𝖤𝗘𝘌𝙀𝙴𝚬𝛦𝜠𝝚𝞔",
        "F": "FϜᖴℱꓝꞘＦ𐊇𐊥𐔥𑢢𑣂𝈓𝐅𝐹𝑭𝓕𝔉𝔽𝕱𝖥𝗙𝘍𝙁𝙵𝟊",
        "G": "GɢԌԍᏀᏳᏻꓖꮐＧ𝐆𝐺𝑮𝒢𝓖𝔊𝔾𝕲𝖦𝗚𝘎𝙂𝙶",
        "H": "HʜΗНнᎻᕼℋℌℍⲎꓧꮋＨ𐋏𝐇𝐻𝑯𝓗𝕳𝖧𝗛𝘏𝙃𝙷𝚮𝛨𝜢𝝜𝞖",
        "J": "JͿЈᎫᒍᴊꓙꞲꭻＪ𝐉𝐽𝑱𝒥𝓙𝔍𝕁𝕵𝖩𝗝𝘑𝙅𝙹",
        "K": "KΚКᏦᛕKⲔꓗＫ𐔘𝐊𝐾𝑲𝒦𝓚𝔎𝕂𝕶𝖪𝗞𝘒𝙆𝙺𝚱𝛫𝜥𝝟𝞙",
        "L": "LʟᏞᒪℒⅬⳐⳑꓡꮮＬ𐐛𐑃𐔦𑢣𑢲𖼖𝈪𝐋𝐿𝑳𝓛𝔏𝕃𝕷𝖫𝗟𝘓𝙇𝙻",
        "M": "MΜϺМᎷᗰᛖℳⅯⲘꓟＭ𐊰𐌑𝐌𝑀𝑴𝓜𝔐𝕄𝕸𝖬𝗠𝘔𝙈𝙼𝚳𝛭𝜧𝝡𝞛",
        "N": "NɴΝℕⲚꓠＮ𐔓𝐍𝑁𝑵𝒩𝓝𝔑𝕹𝖭𝗡𝘕𝙉𝙽𝚴𝛮𝜨𝝢𝞜",
        "P": "PΡРᏢᑭᴘᴩℙⲢꓑꮲＰ𐊕𝐏𝑃𝑷𝒫𝓟𝔓𝕻𝖯𝗣𝘗𝙋𝙿𝚸𝛲𝜬𝝦𝞠",
        "Q": "QℚⵕＱ𝐐𝑄𝑸𝒬𝓠𝔔𝕼𝖰𝗤𝘘𝙌𝚀",
        "R": "RƦʀᎡᏒᖇᚱℛℜℝꓣꭱꮢＲ𐒴𖼵𝈖𝐑𝑅𝑹𝓡𝕽𝖱𝗥𝘙𝙍𝚁",
        "S": "SЅՏᏕᏚꓢＳ𐊖𐐠𖼺𝐒𝑆𝑺𝒮𝓢𝔖𝕊𝕾𝖲𝗦𝘚𝙎𝚂",
        "T": "TΤτТтᎢᴛ⊤⟙ⲦꓔꭲＴ𐊗𐊱𐌕𑢼𖼊𝐓𝑇𝑻𝒯𝓣𝔗𝕋𝕿𝖳𝗧𝘛𝙏𝚃𝚻𝛕𝛵𝜏𝜯𝝉𝝩𝞃𝞣𝞽🝨",
        "U": "UՍሀᑌ∪⋃ꓴＵ𐓎𑢸𖽂𝐔𝑈𝑼𝒰𝓤𝔘𝕌𝖀𝖴𝗨𝘜𝙐𝚄",
        "V": "VѴ٧۷ᏙᐯⅤⴸꓦꛟＶ𐔝𑢠𖼈𝈍𝐕𝑉𝑽𝒱𝓥𝔙𝕍𝖁𝖵𝗩𝘝𝙑𝚅",
        "W": "WԜᎳᏔꓪＷ𑣦𑣯𝐖𝑊𝑾𝒲𝓦𝔚𝕎𝖂𝖶𝗪𝘞𝙒𝚆",
        "X": "XΧХ᙭ᚷⅩ╳ⲬⵝꓫꞳＸ𐊐𐊴𐌗𐌢𐔧𑣬𝐗𝑋𝑿𝒳𝓧𝔛𝕏𝖃𝖷𝗫𝘟𝙓𝚇𝚾𝛸𝜲𝝬𝞦",
        "Y": "YΥϒУҮᎩᎽⲨꓬＹ𐊲𑢤𖽃𝐘𝑌𝒀𝒴𝓨𝔜𝕐𝖄𝖸𝗬𝘠𝙔𝚈𝚼𝛶𝜰𝝪𝞤",
        "Z": "ZΖᏃℤℨꓜＺ𐋵𑢩𑣥𝐙𝑍𝒁𝒵𝓩𝖅𝖹𝗭𝘡𝙕𝚉𝚭𝛧𝜡𝝛𝞕",
    }
    assert len(arg) == 2, "enter 2 methods to choose from."

    method_pick = np.random.choice(len(arg), 1)[0]

    if arg[method_pick] == "unicode":
        char_array = np.array(list(word))

        int_pick = np.random.randint(0, high=unicode_array.shape[0], size=len(word))

        picked_unicode = unicode_array[int_pick]

        perturbed_array = np.char.add(char_array, picked_unicode)
        return "".join(perturbed_array)
    elif arg[method_pick] == "homoglyph":
        char_list = list(word)
        homoglyph_char_list = []
        for char in char_list:
            try:
                glyph_string = d[char]
                glyph_pick = np.random.choice(len(glyph_string), 1)[0]
                homoglyph_char_list.append(glyph_string[glyph_pick])
            except KeyError:
                homoglyph_char_list.append(char)
        return "".join(homoglyph_char_list)


if __name__ == "__main__":
    print(visual_similar_chars("adversarial", "unicode", "homoglyph"))

    
