import numpy as np


def glyph(character):
    """
    return visually similar homoglyph of any character(a-z).

    Input must be single character

    eg:

    input: f

    output: 𝓯

    If a character not present in dictionary is entered,
    input character itself will be returned.

    """
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
    try:
        glyph_string = d[character]
        glyph_pick = np.random.choice(len(glyph_string), 1)[0]
        return glyph_string[glyph_pick]
    except KeyError:
        return character


if __name__ == "__main__":
    print(glyph("f"))
