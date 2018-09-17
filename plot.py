from clustering import *
import os  # for os.path.basename
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
import pandas as pd

class Plot(Clustering):

    def __init__(self, folder=None):
        super().__init__(self)
        self.folder = folder

    def create_MDS(self):
        # convert two components as we're plotting points in a two-dimensional plane
        # "precomputed" because we provide a distance matrix
        # we will also specify `random_state` so the plot is reproducible.
        self.dist = self.distance()
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

        pos = mds.fit_transform(self.dist)  # shape (n_components, n_samples)

        xs, ys = pos[:, 0], pos[:, 1]
        return xs, ys

    def setClusters(self):
        #set up colors per clusters using a dict
        cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

        #set up cluster names using a dict
        cluster_names = {0: 'cluster 0', 
                        1: 'cluster 1', 
                        2: 'cluster 2', 
                        3: 'cluster 3', 
                        4: 'cluster 4'}
        return cluster_colors, cluster_names

    def load_tfidf(self):
        self.tfidf_matrix = joblib.load('tfidf_matrix.pkl')
        self.tfidf_vectorizer = joblib.load('vectorizer.pkl')
        print("TF-IDF Loaded!\n")

    def distance(self):
        self.dist = 1 - cosine_similarity(self.tfidf_matrix)
        return self.dist

    def buildGraph(self):
        self.load_tfidf()
        cPaths = Paths(self.folder)
        self.filenames, self.folders = cPaths.getPdfs()
        xs, ys = self.create_MDS()
        cluster_colors, cluster_names = self.setClusters()
        #some ipython magic to show the matplotlib plots inline

        #create data frame that has the result of the MDS plus the cluster numbers and titles
        df = pd.DataFrame(dict(x=xs, y=ys, label=self.clusters(), title=self.filenames))

        #group by cluster
        groups = df.groupby('label')


        # set up plot
        fig, ax = plt.subplots(figsize=(20, 11)) # set size
        ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

        #iterate through groups to layer the plot
        #note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
        for name, group in groups:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
                    label=cluster_names[name], color=cluster_colors[name], 
                    mec='none')
            ax.set_aspect('auto')
            ax.tick_params(\
                axis= 'x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off')
            ax.tick_params(\
                axis= 'y',         # changes apply to the y-axis
                which='both',      # both major and minor ticks are affected
                left='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelleft='off')
            
        ax.legend(numpoints=1)  #show legend with only 1 point

        #add label in x,y position with the label as the film title
        for i in range(len(df)):
            ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  
    
        plt.show() #show the plot

        #uncomment the below to save the plot if need be
        #plt.savefig('clusters_small_noaxes.png', dpi=200)