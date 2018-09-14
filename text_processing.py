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
        self.documents, self.textOnly = self.docLists()
        self.vectorizer()
        self.the_matrix()
        # for i, text in enumerate(self.documents):
        #     self.text = text[1:][0]

        #     self.the_matrix(i)

        return self.getMatrix()

    def vectorizer(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=200000,
                                 stop_words='english',
                                 use_idf=True, tokenizer=self.tokenize_and_stem, ngram_range=(1,1), norm='l2')

    def the_matrix(self):
        self.tfidf_matrix= self.tfidf_vectorizer.fit_transform(self.textOnly)

    def getMatrixShape(self):
        return self.tfidf_matrix.shape
    
    def getMatrix(self):
        return self.tfidf_matrix
