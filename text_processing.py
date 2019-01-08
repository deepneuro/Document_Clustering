from sklearn.feature_extraction.text import TfidfVectorizer
from pre_processing import *

class TextProcessing(Pre_processing):

    def __init__(self, folder, filenames=None, folders=None, errors=None):
        self.folder = folder
        self.filenames = filenames
        self.folders = folders
        self.errors = errors
        if self.errors == None:
            self.errors = []
        if self.filenames is None:
            self.filenames = []
        if self.folders is None:
            self.folders = []
        super().__init__(self)

    def docs(self):
        self.documents = self.docLists()
        return self.documents

    def corpus(self):
        self.documents, self.textOnly = self.docTxtLists()
        self.vectorizer()
        self.the_matrix()
        return self.getMatrix()

    def vectorizer(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=200000,
                                 stop_words='english',
                                 use_idf=True, tokenizer=self.tokenize_and_stem, ngram_range=(1,1), norm='l2')

    def the_matrix(self):
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.textOnly)

    def getMatrixShape(self):
        return self.tfidf_matrix.shape
    
    def getMatrix(self):
        return self.tfidf_matrix

    def saveTFIDF(self):
        from sklearn.externals import joblib
        joblib.dump(self.getMatrix(), 'tfidf_matrix.pkl')
        joblib.dump(self.tfidf_vectorizer, 'vectorizer.pkl')
        print("\nTF-IDF matrix and model saved!\n")

