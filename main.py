# main functions of the app

# def import_documents():

# def create_keywords():

# def run_search():

import pather
import pdfparser


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
