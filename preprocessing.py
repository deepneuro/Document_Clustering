import csv
import re

import spacy.lang.en
import spacy.lang.pt

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer

# Reading the portuguese stop words
with open('stop_words.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    stop_words_pt = list(reader)
stop_words_pt = [element[1] for element in stop_words_pt][1:]
stop_words_pt = stop_words_pt + ['e']


# ----------------------------------- #
#         Portuguese Section          #
# ----------------------------------- #


def text_tokenization_portuguese(string):
    """
    From a string, returns a list of tokens that are in it
    :param string: String to be tokenized
    :return: a list of tokens
    """
    # Regular expression to match
    re_list = re.findall('([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ-#&-*+]+)', string)
    # Filter by tokens that are more than 2 characters long
    token_list = [element.lower() for element in re_list if len(element) > 2]

    return token_list


# Creating the necessary objects for the following functions to run

# Stemming object (from NLTK)
stemmer_pt = SnowballStemmer("portuguese")

# Lematization dictionary (From SpaCy lib)
first_dict = dict(spacy.lang.pt.lemmatizer.LOOKUP)
lems_pt = {key.lower(): value.lower() for key, value in first_dict.items()}


def text_stemming_portuguese(token_list):
    """
    For a given token list, returns its stems (for portuguese only)
    :param token_list: A list of tokens
    :return: A list of stemmed tokens
    """

    stems_pt = [stemmer_pt.stem(token) for token in token_list]

    return stems_pt


def text_lemmatization_portuguese(token_list):
    """
    For a given token list, returns its lemmas if they exist
    (for portuguese only)
    :param token_list: A list of tokens
    :return: A list of lemmatized tokens
    """

    lemmas_pt = [lems_pt[token] if token in lems_pt else token
                 for token in token_list]

    return lemmas_pt


def text_tokenization_stemming_pt(string):
    """
    For a given string, returns a tokenization result with stemming (for
    portuguese)
    :param string: The string to be tokenized
    :return: a list of stemmed tokens
    """
    tokens = text_tokenization_portuguese(string)
    stems = text_stemming_portuguese(tokens)

    return stems


def text_tokenization_lemmatization_pt(string):
    """
    For a given string, returns a tokenization result with lemmatization (for
    portuguese)
    :param string: The string to be tokenized
    :return: a list of lemmatized tokens
    """
    tokens = text_tokenization_portuguese(string)
    lemmas = text_lemmatization_portuguese(tokens)

    return lemmas


def create_tf_idf_matrix_portuguese(document_series,
                                    token_function=
                                    text_tokenization_portuguese):
    """
    From a pandas series of documents, create its TF-IDF matrix
    :param document_series: pandas series of documents
    :param token_function: function of tokenization to be used by the TF_IDF
    :return: TF-IDF matrix of the documents (sparse)
    """

    TF_IDF_pt = TfidfVectorizer(stop_words=stop_words_pt,
                                tokenizer=token_function,
                                ngram_range=(1, 1))
    tf_idf_matrix = TF_IDF_pt.fit_transform(document_series)

    return tf_idf_matrix, TF_IDF_pt.get_feature_names()


# ----------------------------------- #
#           English Section           #
# ----------------------------------- #

def text_tokenization_english(string):
    """
    From a string, returns a list of tokens that are in it
    :param string: String to be tokenized
    :return: List of tokens
    """
    # Regular expression to match
    re_list = re.findall('([A-Za-zÀ-ÿ\']+)', string)
    # Filter by tokens that are more than 2 characters long
    token_list = [element.lower() for element in re_list if len(element) > 2]

    return token_list


# Creating the necessary objects for the functions to run

# Stemming object (from NLTK)
stemmer_en = SnowballStemmer("english")

# Lemmas dictionary (From SpaCy lib)
first_dict = dict(spacy.lang.en.lemmatizer.LOOKUP)
lems_en = {key.lower(): value.lower() for key, value in first_dict.items()}


def text_stemming_english(token_list):
    """
    For a given token list, returns its stems (for english only)
    :param token_list: A list of tokens
    :return: A list of stemmed tokens
    """

    stems_en = [stemmer_en.stem(token) for token in token_list]

    return stems_en


def text_lemmatization_english(token_list):
    """
    For a given token list, returns its lemmas if they exist
    (for english only)
    :param token_list: A list of tokens
    :return: A list of lemmatized tokens
    """

    lemmas_en = [lems_en[token] if token in lems_pt else token
                 for token in token_list]

    return lemmas_en


def text_tokenization_stemming_en(string):
    """
    For a given string, returns a tokenization result with stemming (for
    english)
    :param string: The string to be tokenized
    :return: A list of stemmed tokens
    """
    tokens = text_tokenization_english(string)
    stems = text_stemming_english(tokens)

    return stems


def text_tokenization_lemmatization_en(string):
    """
    For a given string, returns a tokenization result with lemmatization (for
    english)
    :param string: The string to be tokenized
    :return:  A list of lemmatized tokens
    """
    tokens = text_tokenization_english(string)
    lemmas = text_lemmatization_english(tokens)

    return lemmas


def create_tf_idf_matrix_english(document_series,
                                 token_function=
                                 text_tokenization_english):
    """
    From a pandas series of documents, create its TF-IDF matrix
    :param document_series: pandas series of documents
    :param token_function: function of tokenization to be used by the TF_IDF
    :return: TF-IDF matrix of the documents (sparse)
    """

    TF_IDF_en = TfidfVectorizer(stop_words='english',
                                tokenizer=token_function,
                                ngram_range=(1, 1))
    tf_idf_matrix = TF_IDF_en.fit_transform(document_series)

    return tf_idf_matrix, TF_IDF_en.get_feature_names()
