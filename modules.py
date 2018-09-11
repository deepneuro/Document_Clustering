#%%
from numpy import zeros, asarray, sum
from math import log
import pandas as pd
import sys
import codecs
import re
import glob 
import spacy
import numpy as np
import io
import fileinput
from os import chdir, getcwd, listdir, path, mkdir, walk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from scipy.linalg import svd
from spacy.lang.en.stop_words import STOP_WORDS    
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
import PyPDF2
from langdetect import detect_langs
