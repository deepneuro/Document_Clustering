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


def one_term_search(search_term, TF_IDF_matrix, token_list, num_returns='all'):
    """
    For a given term, returns the tom num_returns documents that contain the
    search term.
    :param search_term: A string, the term to be searched
    :param TF_IDF_matrix: The original TF-IDF matrix (from create_tf_idf_matrix
    method)
    :param token_list: The list of tokens (from create_tf_idf_matrix method)
    :param num_returns: Int; The maximum number of matches to return
    :return: Document number and score for the given term
    """

    search_term = search_term.lower()

    token_index = token_list.index(search_term)  # Find term index

    token_matrix = TF_IDF_matrix[:, token_index]  # Slice matrix to get term

    ordered_matrix = sort_lines(token_matrix)  # Order matrix

    if num_returns == 'all':
        return ordered_matrix
    else:
        return ordered_matrix[0:num_returns]  # Return top N documents


def documents_return(ordered_matrix, document_dataframe):
    """
    For a given document ID, returns the document file name.
    :param ordered_matrix: A matrix in row value form tuple
    :param document_dataframe: The original dataframe with the documents
    :return: List of the name of the files
    """

    document_list = [document_dataframe.iloc[document[0]].file
                     for document in ordered_matrix]
    scores = [ordered_index[1] for ordered_index in ordered_matrix]
    return document_list, scores


def corpus_return(ordered_matrix, document_dataframe):
    """
    For a given document ID, returns the document text. (for summarizer)
    :param ordered_matrix: A matrix in row value form tuple
    :param document_dataframe: The original dataframe with the documents
    :return:  List of the text of the files
    """
    document_list = [document_dataframe.iloc[document[0]].text
                     for document in ordered_matrix]
    return document_list


def normalize_column(ordered_matrix):
    """
    For a given result of search, returns a normalized score (between 1 and 0)
    :param ordered_matrix: (list) Result of a search
    :return: (list) Normalized result of a search
    """

    max_value = ordered_matrix[0][1]
    normalized_matrix = [(row[0], row[1]/max_value) for row in ordered_matrix]

    return normalized_matrix


def sort_lines_to_csc(sorted_lines, TF_IDF_matrix):
    """
    For given lines sorted, return a csc matrix of the result
    :param sorted_lines: result of sorted_lines function
    :return: csc matrix of the result
    """
    data = [line[1] for line in sorted_lines]
    rows = [line[0] for line in sorted_lines]
    cols = [0] * len(sorted_lines)
    final_shape = (TF_IDF_matrix.shape[0], 1)

    csc_matrix = scipy.sparse.csc_matrix((data, (rows, cols)),
                                         shape=final_shape)

    return csc_matrix


def multi_term_search(search_terms, TF_IDF_matrix, token_list,
                      method='mult',
                      num_returns='all'):
    """
    For a given number of terms, returns the documents that have bigger
    frequency of said terms
    :param search_terms: (list) terms to be searched in docuents
    :param TF_IDF_matrix: (scipy.sparse) TF-IDF matrix
    :param token_list: (list) Tokens resulting from TF-IDF transformation
    :param method: (str) either 'add' or 'mult'; Adds or multiplies columns
    :param num_returns: (int) Number of hits wanted
    :return: (list) Top N returns for the given search terms (index and score)
    """

    search_terms = [search_term.lower() for search_term in search_terms]

    ordered_matrices = [one_term_search(search_term, TF_IDF_matrix, token_list)
                        for search_term in search_terms]
    normalized_matrices = [normalize_column(ordered_matrix)
                           for ordered_matrix in ordered_matrices]
    csc_matrices = [sort_lines_to_csc(normalized_matrix, TF_IDF_matrix)
                    for normalized_matrix in normalized_matrices]

    size = TF_IDF_matrix.shape[0]

    if method == 'add':
        sum_matrix = scipy.sparse.csc_matrix((size, 1))
        for csc_matrix in csc_matrices:
            sum_matrix += csc_matrix

        end_matrix = sum_matrix
    elif method == 'mult':
        initial_array = np.array([[1]]*size)
        mult_matrix = scipy.sparse.csc_matrix(initial_array)
        for csc_matrix in csc_matrices:
            mult_matrix = mult_matrix.multiply(csc_matrix)

        end_matrix = mult_matrix
    else:
        return None

    sorted_results = sort_lines(end_matrix)
    normalized_results = normalize_column(sorted_results)
    if num_returns == 'all':
        return normalized_results
    else:
        return normalized_results[:num_returns]
