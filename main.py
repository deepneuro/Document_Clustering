# main functions of the app

# def import_documents():

# def create_keywords():

# def run_search():

import pather
import pdfparser
import reader
import clustering
import preprocessing
import time


def write_txt_documents(path):
    """
    For a given path, writes the .pdf documents separated by language in
    sub-folders as .txt files.
    :param path: Path to find the pdf files
    :return: .txt files
    """

    # Find the .pdf paths
    path_list = pather.find_paths(path, 'pdf')
    # Find the directories
    directory_list = pather.return_first_elements(path_list)
    # Find the files' name
    file_list = pather.return_last_element(path_list)

    exception_list = list()

    for file_index, file in enumerate(path_list):
        try:
            # Parse the pdf
            text = pdfparser.pdf2string(file)
            # Detect the pdf language
            language = pdfparser.detect_language(text)
            # Create the directory for the language detected
            new_directory = directory_list[file_index] + language + '\\'
            pather.create_directory([language], [directory_list[file_index]])

            # Create the path for the .txt file
            text_path = new_directory + file_list[file_index][:-3] + 'txt'
            # Write the parsed pdf to the .txt file
            pdfparser.string2txt(text, text_path)

        except Exception as e:
            exception_list.append([e, file])

    return exception_list


def top_cluster_words(path, num_clusters, num_words, language='pt'):  # TODO Clear times prints
    """
    For a given path, reads the .txt files and creates the top words for each
    cluster, with TF-IDF parametrization
    :param path: Path to the .txt files
    :param num_clusters: number of desired clusters
    :param num_words: number of desired words
    :param language: Language to be analysed
    :return: List with most important words and elements of the cluster
    """
    timer = time.time()
    texts_dataframe = reader.create_data_frame(path)

    print('First task (read txt files):')
    print(time.time()-timer)
    timer = time.time()

    tf_idf_matrix, tokens = preprocessing.create_tf_idf_matrix_portuguese(
        texts_dataframe[texts_dataframe.lang == language].text)
    print('Second task (tf-idf matrix):')
    print(time.time()-timer)
    timer = time.time()

    kmeans_model = clustering.k_means_definition(tf_idf_matrix, num_clusters)
    print('Third task (clustering):')
    print(time.time()-timer)
    timer = time.time()

    top_words = clustering.top_terms(kmeans_model, tokens, num_words,
                texts_dataframe[texts_dataframe.lang == language].file.tolist())

    print('Fourth task (finding words):')
    print(time.time()-timer)

    return top_words


if __name__ == '__main__':
    top_cluster_words(r'C:\Users\sergiojesus\Desktop\Coisas da Alvita\CV')

class SearchEngine(init_path)
    self.path = init_path
