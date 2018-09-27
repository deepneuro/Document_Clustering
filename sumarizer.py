import re
from gensim.summarization.summarizer import summarize


def line_parser(string):
    """
    TODO
    :param file:
    :return:
    """

    pattern = '-|- \n|-|-\n|- |–|•|\no'
    line_list = re.sub(pattern, ' ', string).split('\n')

    result = [item.strip() for item in line_list if len(item.strip()) > 2]

    return result


def clean_lines(res):
    """
    TODO
    :param res:
    :return:
    """
    for element in res[1:]:
        letter = element[0]
        if letter.islower() or element.split()[0] == 'Aveiro' or element.split()[0] == 'After':
            res[res.index(element)-1] += ' ' + element
            del res[res.index(element)]
    return res


def create_text(lines):
    """
    TODO
    :param lines:
    :return:
    """
    return '\n'.join(lines)


def summarization(text):
    """
    TODO
    :param text:
    :return:
    """
    summarized_text = summarize(text, word_count=100)

    return list(set(summarized_text))
