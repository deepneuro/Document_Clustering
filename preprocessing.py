import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer


# Reading the portuguese stop words
with open('stop_words.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    stop_words_pt = list(reader)
stop_words_pt = [element[1] for element in stop_words_pt][1:]
stop_words_pt = stop_words_pt + ['e']


def text_tokenization_portuguese(string):
    """
    From a string, returns a list of tokens that are in it
    :param string: String to be tokenized
    :return: List of tokens
    """
    re_list = re.findall('([A-Za-zÀ-ÿ]+(-|)[A-Za-zÀ-ÿ]+|[A-Za-zÀ-ÿ]+)', string)

    token_list = [element[0] for element in re_list]

    return token_list


# Creating the TF-IDF vectorizer class
TF_IDF = TfidfVectorizer(stop_words=stop_words_pt,
                         tokenizer=text_tokenization_portuguese,
                         ngram_range=(1, 2))


def create_tf_idf_matrix(document_series):
    """
    From a pandas series of documents, create its TF-IDF matrix
    :param document_series: pandas series of documents
    :return: TF-IDF matrix of the documents (sparse)
    """

    tf_idf_matrix = TF_IDF.fit_transform(document_series)

    return tf_idf_matrix, TF_IDF.get_feature_names()


