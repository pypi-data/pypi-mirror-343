"""
functions to deal with string and text

"""
import random


def markup(string, index, length, markup_left='', markup_right=''):
    """
    to add some markup labels to the string to make it a rich format
    :param string: str. the original string
    :param index: int. the starting index
    :param length: int. the length from the staring index
    :param markup_left: str. add markup language like <strong>, default to ''
    :param markup_right: str. add markup language like </strong>, default to ''
    :return: a new string
    """
    new_string = string[:index] + markup_left + string[index: index + length:] + markup_right + string[index + length:]
    return new_string


def randomMarkupChar(string, markup_ratio=.5, markup_left='', markup_right='', random_seed=None):
    """
    randomly markup chars of a text
    :param string: old text
    :param markup_ratio: the ratio of markup
    :param markup_left:
    :param markup_right:
    :param random_seed: random seed, default to None
    :return a new text
    """
    new_string = string
    total = len(string)
    markup_total = int(total * markup_ratio)
    rand = random.Random()
    if random_seed:
        rand.seed(random_seed)
    markup_index = rand.sample(range(total), k=markup_total)

    for i in markup_index:
        new_string = markup(new_string, i, 1, markup_left, markup_right)

    return new_string


def randomMarkupWord(string, markup_ratio=.5, markup_left='', markup_right='', random_seed=None):
    """
    randomly markup words of a text
    :param string: old text
    :param markup_ratio: the ratio of markup
    :param markup_left:
    :param markup_right:
    :param random_seed: random seed, default to None
    :return a new text
    """
    words_list = string.split(' ')
    total = len(words_list)
    markup_total = int(total * markup_ratio)
    rand = random.Random()
    if random_seed:
        rand.seed(random_seed)
    markup_index = rand.sample(range(total), k=markup_total)
    for i in markup_index:
        word = words_list[i]
        words_list[i] = markup(word, 0, len(word), markup_left, markup_right)
    new_string = ' '.join(words_list)

    return new_string

def randomMarkupText(string, markup_ratio=.5, markup_left='', markup_right='', random_seed=None):
    """
    distinguish English from Chinese:
        if English, use word markup
        if Chinese, use char markup
    :param string:
    :param markup_ratio:
    :param markup_left:
    :param markup_right:
    :param random_seed:
    :return: a new text
    """
    if string.isascii():
        return randomMarkupWord(string, markup_ratio=.5, markup_left='', markup_right='', random_seed=None)
    else:
        return randomMarkupChar(string, markup_ratio=.5, markup_left='', markup_right='', random_seed=None)


def splice(string, index, length, new_str):
    """
    take a string, replacing a certain parts of it starting from the
    index with new_str
    if length = 0, it's just a inserting new_str
    if length = len(new_str), it's substitution
    inspired by javascrip 'splice'.
    :param string: str. the original string
    :param index: int. the starting index
    :param length: int. the length from the staring index
    :param new_str: str. the new string inserted or to override
    :return: a new string
    """
    new_string = string[:index] + new_str + string[index + length:]
    return new_string


def randomSpliceText(string, sub_char='*', sub_ratio=.5, random_seed=None):
    """
    distinguish English from Chinese:
        if English, use word substitution
        if Chinese, use char substitution
    :param string:
    :param sub_char:
    :param sub_ratio:
    :param random_seed:
    :return: a new text
    """
    if string.isascii():
        return randomSpliceWord(string, sub_char, sub_ratio, random_seed)
    else:
        return randomSpliceChar(string, sub_char, sub_ratio, random_seed)


def randomSpliceChar(string, sub_char='*', sub_ratio=.5, random_seed=None):
    """
    randomly substitute chars of a text
    :param string: old text
    :param sub_char: single char to replace the word's letter
    :param sub_ratio: the ratio of substitution
    :param random_seed: random seed, default to None
    :return a new text
    """
    new_string = string
    total = len(string)
    sub_total = int(total * sub_ratio)
    rand = random.Random()
    if random_seed:
        rand.seed(random_seed)
    sub_index = rand.sample(range(total), k=sub_total)
    # do not substitute '\n'
    for i in sub_index:
        if new_string[i] != '\n':
            new_string = splice(new_string, i, 1, new_str=sub_char)

    return new_string


def randomSpliceWord(string, sub_char='*', sub_ratio=.5, random_seed=None):
    """
    randomly substitute text of English words
    :param string: old text
    :param sub_char: single char to replace the word's letter
    :param sub_ratio: the ratio of substitution
    :param random_seed: random seed, default to None
    :return: a new text
    """
    words_list = string.split(' ')
    total = len(words_list)
    sub_total = int(total * sub_ratio)
    rand = random.Random()
    if random_seed:
        rand.seed(random_seed)
    sub_index = rand.sample(range(total), k=sub_total)
    for i in sub_index:
        word = words_list[i]
        # deal with '\n'
        if word.endswith('\n'):
            words_list[i] = splice(word, 0, len(word), new_str=sub_char * (len(word) - 1)) + '\n'
        else:
            words_list[i] = splice(word, 0, len(word), new_str=sub_char * len(word))
    new_string = ' '.join(words_list)
    return new_string

def python2cppCode(code):
    # turn python code to c++ code
    cppcode = code.replace("'", "\"") \
               .replace("self.", "") \
               .replace("self", "")\
               .replace(",self", "")\
               .replace(", self", "") \
               .replace("#", "//")\
               .replace("//include", "#include")\
               .replace("// include", "# include")\
               .replace(".", "->")\
               .replace("->h\"", ".h\"")\
               .replace("->h>", ".h>")\
               .replace("True", "true")\
               .replace("False", "false")\
               .replace(")\n", ");\n")
    with open('code.txt', 'w') as f:
        f.write(cppcode)
    return cppcode


if __name__ == '__main__':
    old = ("""I love  china, it's a great country """)
    # print(splice(old,3,2,'**'))
    # print(splice(old,3,0,'**'))
    # print(splice(old,30,2,'**'))
    # print(splice(old,50,2,'**'))
    print(old)
    # print(randomSpliceWord(old, ' ', .5, ))

    print(markup(old, 4, 4, '<strong>', '</strong>'))
    print(randomMarkupChar(old, .5, '<color>', "</color>", 1))
    print(randomMarkupWord(old, .5, '<color>', "</color>", 1))
