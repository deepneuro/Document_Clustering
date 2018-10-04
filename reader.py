import pandas as pd
import pather


def find_txt_files(initial_path):
    """
    For a given path, returns the paths to the .txt files
    :param initial_path: the initial directory of search
    :return: list of paths inside the initial path
    """

    path_list = pather.find_paths(initial_path, "txt")

    last_elements = pather.return_last_element(path_list)

    first_elements = pather.return_first_elements(path_list)

    return path_list, last_elements, first_elements


def read_txt_file(path):
    """
    For a given .txt path, reads the file and returns a string
    :param path: The path to the .txt file
    :return: string of the file
    """

    file = open(path, "r", encoding='utf-8')
    text_string = file.read()

    return text_string


def create_dir(first_element):
    """
    TODO
    :param first_element:
    :return:
    """
    first_elements_list = first_element.split('\\')
    for index, element in enumerate(first_elements_list):
        if element == 'CV' or element == 'cv':
            path = '\\'.join(first_elements_list[index:])
    return path


def create_filename(last_element):
    """
    TODO
    :param last_element:
    :return:
    """
    return last_element[:-4]


def create_data_frame(initial_path):
    """
    For a given path, returns a dataframe with the document name of the document
    language and text.
    :param initial_path: path with the .txt files
    :return: dataframe with the mentioned fields
    """

    path_list, last_elements, first_elements = find_txt_files(initial_path)

    lang = [element.split('\\')[-2] for element in first_elements]

    text_files = [read_txt_file(file) for file in path_list]

    dirs = [create_dir(first_element) for first_element in first_elements]

    name = [create_filename(last_element) for last_element in last_elements]

    dataframe_dict = {'file': last_elements, 'lang': lang, 'text': text_files,
                      'dir': dirs, 'names': name}

    dataframe = pd.DataFrame(dataframe_dict)

    return dataframe
