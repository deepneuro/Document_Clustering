from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import pandas as pd
from text_processing import *

class Clustering(TextProcessing):

    def __init__(self, folder, num_clusters=None, documents=None):
        super().__init__(self, documents)
        self.folder = folder
        self.documents = documents
        self.num_clusters = num_clusters
        if self.num_clusters is None:
            self.num_clusters = 4

    def getTerms(self):
        terms = self.tfidf_vectorizer.get_feature_names()
        return terms

    def getVocabFrame(self):
        totalvocab_tokenized, totalvocab_stemmed, lemma = self.text_process()
        vocab_frame = pd.DataFrame({'words': lemma}, index = lemma)
        return vocab_frame

    def distance(self):
        self.dist = 1 - cosine_similarity(self.tfidf_matrix)
        
    def k_means(self):
        self.km = KMeans(n_clusters=self.num_clusters)
        self.km.fit(self.tfidf_matrix)

    def clusters(self):
        self.k_means()
        clusters = self.km.labels_.tolist()
        return clusters

    def dump_Kmeans(self):
        from sklearn.externals import joblib
        joblib.dump(self.km, 'doc_cluster.pkl')

    def load_Kmeans(self):
        self.km = joblib.load('doc_cluster.pkl')
        clusters = self.km.labels_.tolist()
        return clusters

    def load_tfidf(self):
        self.tfidf_matrix = joblib.load('tfidf_matrix.pkl')
        self.tfidf_vectorizer = joblib.load('vectorizer.pkl')
        print("TF-IDF Loaded!\n")

    def matrix2dataframe(self):
        cPaths = Paths(self.folder)
        self.filenames, self.folders = cPaths.getTxts()
        self.documents, self.textOnly = self.docTxtLists()
        docs_dict = { 'filename': self.filenames, 'txt': self.textOnly, 'cluster': self.clusters() }
        frame = pd.DataFrame(docs_dict, index = [self.clusters()] , columns = ['filename', 'cluster'])
        return frame

    def top_terms(self):
        frame = self.matrix2dataframe()
        terms = self.getTerms()
        vocab_frame = self.getVocabFrame()

        print("Top terms per cluster:")
        print()
        #sort cluster centers by proximity to centroid
        order_centroids = self.km.cluster_centers_.argsort()[:, ::-1]

        for i in range(self.num_clusters):
            print("Cluster %d words:" % i, end='')
            for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
                print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
            print() #add whitespace
            print() #add whitespace
            print("Cluster %d Filenames:" % i, end='')
            for title in frame.ix[i]['filename'].values.tolist():
                print(' %s,' % title, end='')
            print() #add whitespace
            print() #add whitespace
        print()
        print()
        