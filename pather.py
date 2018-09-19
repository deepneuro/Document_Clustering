import os
import glob

# Main objective:
# From a path, return all the pdf files' paths and separate the variables (done)
# Create inside these paths a directory for .txt files.


def find_paths(initial_path, extension):
    """
    From a path, return all the  files of a given extension inside.
    :param initial_path: the initial directory of search
    :param extension: the extension of the files to be searched
    :return: list of paths inside the initial path
    """

    paths = glob.glob(initial_path+r'/**/*.' + extension, recursive=True)

    return paths


def return_last_element(paths):
    """
    From a list of paths, return the element of each path (file).
    :param paths: a list of strings of directories
    :return: a list of strings of the last element of each path (files)
    """
    last_elements = [path.split('\\')[-1] for path in paths]

    return last_elements


def return_first_elements(paths):
    """
    From a list of paths, return the first elements of each path (directory).
    :param paths: a list of strings of directories
    :return: a list of strings of the first elements of each path (directories)
    """

    first_elements = ['\\'.join(path.split('\\')[:-1]) + '\\' for path in paths]

    return first_elements


def create_directory(paths, directories):
    """
    From a list of paths, create inside each path a group of subdirectories.
    :param paths: paths to have new directories
    :param directories: new directories to be added
    :return: Directory created
    """

    for directory in directories:
        for path in paths:
            new_path = directory + path
            try:  # Try to make the desired path
                os.makedirs(new_path)
            except OSError:  # Passes if the path already exists
                pass
