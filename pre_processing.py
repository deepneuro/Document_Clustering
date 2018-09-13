import nltk, spacy, re
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import spacy.lang.en.stop_words, spacy.lang.pt.stop_words, spacy.lang.en.lemmatizer, spacy.lang.pt.lemmatizer
import pickle
from parser2txt import *

class Pre_processing(Parser2txt):

    def __init__(self, documents=None, lang=None):
        self.documents = documents
        self.lang = lang
        if self.documents is None:
            self.documents = []

    def preparation(self):
        # nlp = spacy.load('xx')
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')

    def getStemmed(self):
        return self.totalvocab_stemmed

    def getTokenized(self):
        return self.totalvocab_tokenized

    def saveObjs(self):
        with open('objs.pkl', 'wb') as f:
            pickle.dump([self.getTokenized(), self.getStemmed(), self.lemma], f)

    def loadObjs(self):
        with open('objs.pkl', 'rb') as f:
            self.totalvocab_tokenized, self.totalvocab_stemmed, self.lemma = pickle.load(f)
        return self.totalvocab_tokenized, self.totalvocab_stemmed, self.lemma

    def tokenize_and_stem(self, text, lemmatize=True):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if self.lang == "pt":
                stemmer = SnowballStemmer("portuguese")
                if re.search('[a-zA-Z]', token) and token not in spacy.lang.pt.stop_words.STOP_WORDS and len(token)>2:
                    filtered_tokens.append(token)
            elif self.lang == "en":
                stemmer = SnowballStemmer("english")
                if re.search('[a-zA-Z]', token) and token not in spacy.lang.en.stop_words.STOP_WORDS and len(token)>2:
                    filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        if lemmatize:
            print("Applying Lemmatizer...")
            self.lemmaDoc = self.lemmatizer(stems)
            return self.lemmaDoc
        return stems

    def tokenize_only(self, text, lemmatize=False):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if self.lang == "pt":
                if re.search('[a-zA-Z]', token) and token not in spacy.lang.pt.stop_words.STOP_WORDS and len(token)>2:
                    filtered_tokens.append(token)
            elif self.lang == "en":
                if re.search('[a-zA-Z]', token) and token not in spacy.lang.en.stop_words.STOP_WORDS and len(token)>2:
                    filtered_tokens.append(token)
        if lemmatize:
            self.lemmaDoc = self.lemmatizer(filtered_tokens)
            return self.lemmaDoc
        return filtered_tokens

    def lemmatizer(self, tokens):
        # wordnet_lemmatizer = WordNetLemmatizer()
        # lemma = [wordnet_lemmatizer.lemmatize(x) for x in tokens]
        lemma = []
        if self.lang == "en":
            lems = dict(spacy.lang.en.lemmatizer.LOOKUP)
            for token in tokens:
                if token in lems: lemma.append(lems[token])
                else: lemma.append(token)
        elif self.lang == "pt":
            lems = dict(spacy.lang.pt.lemmatizer.LOOKUP)
            for token in tokens:
                if token in lems: lemma.append(lems[token])
                else: lemma.append(token)
        return lemma

    def text_process(self, stem=True, lemma=True):
        self.totalvocab_stemmed = []
        self.totalvocab_tokenized = []
        self.lemma = []
        # self.stopwords = nltk.corpus.stopwords.words('english')

        for i in range(len(self.documents)):
            self.lang = self.langDetector(i)
            for text in self.documents[i][1:]:
                if stem:
                    if self.lang == "en" and lemma:
                        allwords_stemmed = self.tokenize_and_stem(text, stemmer) #for each item in 'synopses', tokenize/stem
                        self.totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
                        lemma = self.lemmatizer(self.totalvocab_stemmed)
                        self.lemma.extend(lemma)

                    elif self.lang == "pt":
                        stemmer = SnowballStemmer("portuguese")
                        allwords_stemmed = self.tokenize_and_stem(text, stemmer) #for each item in 'synopses', tokenize/stem
                        self.totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
                        lemma = self.lemmatizer(self.totalvocab_stemmed)
                        self.lemma.extend(lemma)
                else:
                    allwords_tokenized = self.tokenize_only(text)
                    self.totalvocab_tokenized.extend(allwords_tokenized)
                    if lemma:
                        lemma = self.lemmatizer(self.totalvocab_tokenized)
                        self.lemma.extend(lemma)
        print('Text Processing successful!')

