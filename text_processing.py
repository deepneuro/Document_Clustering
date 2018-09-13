from sklearn.feature_extraction.text import TfidfVectorizer
from pre_processing import *

class TextProcessing(Pre_processing):

    def __init__(self, folder, filenames=None, folders=None):
        self.filenames = filenames
        self.folder = folder
        self.folders = folders
        if self.filenames is None:
            self.filenames = []
        if self.folders is None:
            self.folders = []
        super().__init__(self)

    def docs(self):
        self.documents = self.docLists()
        return self.documents

    def corpus(self):
        self.documents = self.docLists()   
        for i, text in enumerate(self.documents):
            self.text = text[1:][0]
            self.vectorizer(i)
            self.the_matrix(i)
        return self.getMatrix()

    def vectorizer(self, i):
        self.lang = self.langDetector(i)
        if self.lang == "en":
            self.tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=self.tokenize_and_stem, ngram_range=(1,1), norm='l2')
            return self.tfidf_vectorizer
        elif self.lang == "pt":
            self.tfidf_vectorizer = TfidfVectorizer(max_df=1, max_features=200000,
                                 min_df=0.1, stop_words='english',
                                 use_idf=True, tokenizer=self.tokenize_and_stem, ngram_range=(1,1), norm='l2')
            return self.tfidf_vectorizer

    def the_matrix(self,i):
        self.tfidf_matrix = self.vectorizer(i).fit_transform([self.text])

    def getMatrixShape(self):
        return self.tfidf_matrix.shape
    
    def getMatrix(self):
        return self.tfidf_matrix
