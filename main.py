import pather
import pdfparser
import reader
import clustering
import preprocessing
import searcher
import summarizer
import pandas as pd
from IPython.display import display


def pretty_print(df):
    print_df = df.style.format({'Link': make_clickable})
    display(print_df)


def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)


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


def top_cluster_words(path, num_clusters, num_words, language='pt'):
    """
    For a given path, reads the .txt files and creates the top words for each
    cluster, with TF-IDF parametrization
    :param path: Path to the .txt files
    :param num_clusters: number of desired clusters
    :param num_words: number of desired words
    :param language: Language to be analysed
    :return: List with most important words and elements of the cluster
    """

    texts_dataframe = reader.create_data_frame(path)

    tf_idf_matrix, tokens = preprocessing.create_tf_idf_matrix_portuguese(
        texts_dataframe[texts_dataframe.lang == language].text)

    kmeans_model = clustering.k_means_definition(tf_idf_matrix, num_clusters)

    top_words = clustering.top_terms(kmeans_model, tokens, num_words,
                texts_dataframe[texts_dataframe.lang == language].file.tolist())

    return top_words


class SearchEngine:

    def __init__(self, init_path, lang='pt'):

        self._path = init_path
        self.lang = lang
        self._search_results = None
        self._tokens = None
        self._tf_idf_matrix = None
        self._result_documents = None
        self._dataframe = None
        self._result_summaries = None
        self._result_score = None
        self._paths = None
        self._results = list()

    def _create_df(self):

        self._dataframe = reader.create_data_frame(self._path)
        self._search_dataframe = self._dataframe[self._dataframe.lang == self.lang]

    def _create_tf_idf(self):

        if self._dataframe is None:
            self._create_df()

        if self.lang == 'pt':
            self._tf_idf_matrix, self._tokens = preprocessing.create_tf_idf_matrix_portuguese(self._search_dataframe.text)
        elif self.lang == 'en':
            self._tf_idf_matrix, self._tokens = preprocessing.create_tf_idf_matrix_english(self._search_dataframe.text)

    def _create_results_df(self, search_results):
        print('Results:')
        if len(search_results[0]) == 5:
            filenames = [search_result[0] for search_result in search_results]
            paths = [search_result[1][:-3] for search_result in search_results]
            links = [paths[i] + filenames[i]+'.pdf' for i in range(len(filenames))]
            scores = [search_result[2] for search_result in search_results]
            summaries = [search_result[3] for search_result in search_results]
            results = [search_result[4] for search_result in search_results]
            dataframe = pd.DataFrame({'File': filenames, 'Link': links, 'Score': scores, 'Summary': summaries, 'Results': results})
        else:
            filenames = [search_result[0] for search_result in search_results]
            paths = [search_result[1][:-3] for search_result in search_results]
            links = [paths[i] + filenames[i] + '.pdf' for i in
                     range(len(filenames))]
            scores = [search_result[2] for search_result in search_results]
            dataframe = pd.DataFrame({'File': filenames, 'Link': links, 'Score': scores})
        pd.set_option('display.max_colwidth', -1)

        pretty_print(dataframe)

    def run_search(self, terms, summary=True, num_returns='all'):
        self._results = list()
        if self._tf_idf_matrix is None:
            self._create_tf_idf()

        self._search_results = searcher.multi_term_search(terms,
                                                          self._tf_idf_matrix,
                                                          self._tokens,
                                                          num_returns=num_returns)

        self._result_documents, self._result_score, self._paths = searcher.documents_return(self._search_results, self._search_dataframe)

        if summary:
            result_texts = searcher.corpus_return(self._search_results, self._search_dataframe)
            self._result_summaries = [summarizer.create_summary(result_text) for result_text in result_texts]
            self._found_keywords = [summarizer.create_keywords_text(result_text, terms) for result_text in result_texts]
            for index in range(len(self._result_documents)):
                self._results.append((self._result_documents[index], self._paths[index], self._result_score[index],  self._result_summaries[index], self._found_keywords[index]))

        else:
            for index in range(len(self._result_documents)):
                self._results.append((self._result_documents[index], self._paths[index], self._result_score[index]))
        self._create_results_df(self._results)
        return self._results



