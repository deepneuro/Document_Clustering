import re
from gensim.summarization.summarizer import summarize


def line_parser(string):
    """
    For a string, creates a list with different lines of the text
    :param string: string, the string to be processed
    :return: list, different lines of text
    """

    pattern = '-|- \n|-|-\n|- |–|•|\no '
    line_list = re.sub(pattern, ' ', string).split('\n')

    result = [item.strip() for item in line_list if len(item.strip()) > 2]

    return result


def clean_lines(res):
    """
    Joins lines that start with a lowercase to the previous line
    :param res: List of strings, string separated by line
    :return: List of strings, with joined lines
    """
    for element in res[1:]:
        letter = element[0]
        if letter.islower() or element.split()[0] == 'Aveiro' or element.split()[0] == 'After':
            res[res.index(element)-1] += ' ' + element
            del res[res.index(element)]
    return res


def create_text(lines):
    """
    For a list of strings, creates a single string with elements of list
    separated by line
    :param lines: list of strings
    :return: string
    """
    return '\n'.join(lines)


def summarization(text):
    """
    GenSim summarizer for text
    :param text: text to be summarized
    :return: summarized text
    """
    summarized_text = summarize(text, word_count=50).split('\n')

    return list(set(summarized_text))


def create_summary(text):
    """
    for a given string returns the summary with previous methods.
    (This is optimized to CVs)
    :param text: the text of the CV to be summarized
    :return: summary of the CV
    """

    split_list = line_parser(text)
    parsed_list = clean_lines(split_list)
    joined_text = create_text(parsed_list)
    summaries = summarization(joined_text)

    return create_text(summaries)
