import numpy as np
import scipy


def sort_lines(csr_matrix):
    """
    Given a column matrix, returns itself sorted in a descending way
    :param csr_matrix: The matrix resulting from TF-IDF transformation and
    column slicing (token identification)
    :return: sorted matrix in tuple fashion (row, value)
    """

    csc_matrix = csr_matrix.tocsc()  # Transform to CSC to manipulate lines

    tuples = zip(csc_matrix.indices, csc_matrix.data)

    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def one_token_search(search_term, TF_IDF_matrix, token_list, num_returns=10):
    """
    For a given term, returns the tom num_returns documents that contain the
    search term.
    :param search_term: A string, the term to be searched
    :param TF_IDF_matrix: The original TF-IDF matrix (from create_tf_idf_matrix
    method)
    :param token_list: The list of tokens (from create_tf_idf_matrix method)
    :param num_returns: The maximum number of matches to return
    :return: Document number and score for the given term
    """

    token_index = token_list.index(search_term)  # Find term index

    token_matrix = TF_IDF_matrix[:, token_index]  # Slice matrix to get term

    ordered_matrix = sort_lines(token_matrix)  # Order matrix

    return ordered_matrix[0:num_returns]  # Return top N documents


def cv_return(ordered_matrix, document_dataframe):
    document_list = list()
    for document in ordered_matrix:
        print(document[0])
        document_list.append(document_dataframe.iloc[document[0]].file)


    return document_list