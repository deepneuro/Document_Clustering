
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from langdetect import detect


def pdf2string(path):
    """
    From a given pdf path, it creates a string of the pdf.
    :param path: Path to the pdf file
    :return: string of the pdf file
    """

    file_in = open(path, 'rb')
    # Create a PDF interpreter object. (pdfminer)
    retstr = io.StringIO()
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process each page contained in the document.
    for page in PDFPage.get_pages(file_in):
        interpreter.process_page(page)

    data = retstr.getvalue()

    return data


def string2txt(string, path):
    """
    From a given string, creates a .txt file on the given path.
    :param string: The string to be converted to .txt
    :param path: The path of the .txt file
    :return: File created
    """

    # Writes the string with the encoding wanted
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(string)
        file_out.close()


def detect_language(string):
    """
    For a given string, returns the language it is writen in.
    :param string: the string to be analysed
    :return: the language detected (string)
    """
    return detect(string)