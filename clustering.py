import sys
import pandas as pd
from sklearn.externals import joblib
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


def k_means_definition(tf_idf_matrix, n_clusters):
    """
    Trains a new K_means model for a TF-IDF matrix.
    :param tf_idf_matrix: Sparse matrix of TF-IDF for documents
    :param n_clusters: Number of clusters to create
    :return: Fitted model
    """
    k_means_model = KMeans(n_clusters=n_clusters)

    k_means_model.fit(tf_idf_matrix)

    return k_means_model


def top_terms(k_means_model, token_list, keywords_number, txt_files):
    """
    For a given KMeans fitted model, returns the most important tokens for its
    definition.
    :param k_means_model: KMeans model
    :param token_list: TF-IDF feature names
    :param keywords_number: Number of keywords to return
    :param txt_files: Files where the TF-IDF was processed
    :return: Top TF-IDF feature names
    """

    n_clusters = k_means_model.n_clusters
    ordered_centroids = k_means_model.cluster_centers_.argsort()[:, ::-1]
    word_list = list()
    files_dataframe = cluster_file_dataframe(k_means_model, txt_files)

    for cluster_number in range(n_clusters):
        cluster_string = "Cluster {}".format(cluster_number)

        token_strings = [token_list[word_number] for word_number in
                         ordered_centroids[cluster_number, :keywords_number]]

        word_list.append([cluster_string]+token_strings)

        files = files_dataframe.ix[cluster_number]['filename'].values.tolist()

        word_list.append(['File Names of Cluster {}'.format(cluster_number)] +
                         files)

    return word_list


def cluster_file_dataframe(k_means_model, txt_files):
    """
    Creates a matrix with the cluster each file is in.
    :param k_means_model: The clustering model (KMeans)
    :param txt_files: The text files used
    :return: a dataframe with the cluster of each text file
    """
    dataframe_dict = {'filename': txt_files,
                      'cluster': k_means_model.labels_.tolist()}

    dataframe = pd.DataFrame(dataframe_dict,
                             index=[k_means_model.labels_.tolist()],
                             columns=['filename', 'cluster'])

    return dataframe
