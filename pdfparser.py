
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import time



def pdf2string(path):
    """
    From a given pdf path, it creates a string of the pdf.
    :param path: Path to the pdf file
    :return: string of the pdf file
    """

    fp = open(path, 'rb')
    # Create a PDF interpreter object.
    retstr = io.StringIO()
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process each page contained in the document.
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)

    data = retstr.getvalue()

    return data

