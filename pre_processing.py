import nltk, spacy, re
from nltk.stem.snowball import SnowballStemmer
import pickle
from parser2txt import *


class Pre_processing(Parser2txt):

    def __init__(self, documents=None, lang=None):
        self.documents = documents
        self.lang = lang
        if self.documents is None:
            self.documents = []
        

    def preparation(self):
        nlp = spacy.load('xx')
        nltk.download('stopwords')
        nltk.download('punkt')

    def tokenize_and_stem(self, text,stemmer):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

    def tokenize_only(self,text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens


    def text_process(self, stem=True):
        self.totalvocab_stemmed = []
        self.totalvocab_tokenized = []
        # self.stopwords = nltk.corpus.stopwords.words('english')

        for i in range(len(self.documents)):
            self.lang = self.langDetector(i)
            for text in self.documents[i][1:]:
                if stem:
                    if self.lang == "en":
                        stemmer = SnowballStemmer("english")
                        allwords_stemmed = self.tokenize_and_stem(text, stemmer) #for each item in 'synopses', tokenize/stem
                        self.totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
                    elif self.lang == "pt":
                        stemmer = SnowballStemmer("portuguese")
                        allwords_stemmed = self.tokenize_and_stem(text, stemmer) #for each item in 'synopses', tokenize/stem
                        self.totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
                else:
                    allwords_tokenized = self.tokenize_only(text)
                    self.totalvocab_tokenized.extend(allwords_tokenized)
        print('Text Processing successful!')

    def getStemmed(self):
        return self.totalvocab_stemmed

    def getTokenized(self):
        return self.totalvocab_tokenized

    def saveObjs(self):
        with open('objs.pkl', 'wb') as f:
            pickle.dump([self.getTokenized(), self.getStemmed()], f)

    def loadObjs(self):
        with open('objs.pkl', 'rb') as f:
            self.totalvocab_tokenized, self.totalvocab_stemmed = pickle.load(f)
        return self.totalvocab_tokenized, self.totalvocab_stemmed
