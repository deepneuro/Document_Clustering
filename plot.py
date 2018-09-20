from clustering import *
import os  # for os.path.basename
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
import pandas as pd
import mpld3
import time

class Plot(Clustering):

    def __init__(self, folder=None):
        super().__init__(self)
        self.folder = folder

    def create_MDS(self):
        # convert two components as we're plotting points in a two-dimensional plane
        # "precomputed" because we provide a distance matrix
        # we will also specify `random_state` so the plot is reproducible.
        t0 = time()
        self.dist = self.distance()
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(self.dist)  # shape (n_components, n_samples)
        t1 = time()
        print("MDS: %.2g sec" % (t1 - t0))
        xs, ys = pos[:, 0], pos[:, 1]
        self.saveMDS(xs, ys)
        return xs, ys
    
    def saveMDS(self, xs, ys):
        from sklearn.externals import joblib
        joblib.dump([xs,ys], 'mds.pkl')
        print("saved xs and ys from MDS.fit_transform()")

    def loadMDS(self):
        from sklearn.externals import joblib
        xs, ys = joblib.load('mds.pkl')
        print("loaded xs and ys from MDS.fit_transform()")
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
        self.filenames, self.folders = cPaths.getTxts()
        print("Got filenames and folders")
        xs, ys = self.loadMDS()
        # xs, ys = self.create_MDS()
        print("MDS created!")
        cluster_colors, cluster_names = self.setClusters()
        #some ipython magic to show the matplotlib plots inline
        print("Cluster set created!")
        #create data frame that has the result of the MDS plus the cluster numbers and titles
        df = pd.DataFrame(dict(x=xs, y=ys, label=self.clusters(), title=self.filenames))
        print("Dataset created!")
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

    def buildGraph2(self):
        import toptoolbar
        self.load_tfidf()
        cPaths = Paths(self.folder)
        self.filenames, self.folders = cPaths.getTxts()
        xs, ys = self.loadMDS()
        # xs, ys = self.create_MDS()
        cluster_colors, cluster_names = self.setClusters()

        #create data frame that has the result of the MDS plus the cluster numbers and titles
        
        # df = pd.DataFrame(dict(x=xs, y=ys, label=self.clusters(), title=self.filenames))
        # df.to_csv(self.folder + "/graph_data.csv", sep=",")
        df = pd.read_csv(self.folder + "/graph_data.csv")

        #group by cluster
        groups = df.groupby('label')
        print("\nploting...")
        #define custom css to format the font and to remove the axis labeling
        css = """
        text.mpld3-text, div.mpld3-tooltip {
        font-family:Arial, Helvetica, sans-serif;
        }

        g.mpld3-xaxis, g.mpld3-yaxis {
        display: none; }

        svg.mpld3-figure {
        margin-left: -200px;}
        """

        # Plot 
        fig, ax = plt.subplots(figsize=(14,6)) #set plot size
        ax.margins(0.03) # Optional, just adds 5% padding to the autoscaling

        #iterate through groups to layer the plot
        #note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
        for name, group in groups:
            points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, 
                            label=cluster_names[name], mec='none', 
                            color=cluster_colors[name])
            ax.set_aspect('auto')
            labels = [i for i in group.title]
            
            #set tooltip using points, labels and the already defined 'css'
            tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
                                            voffset=10, hoffset=10, css=css)

            print("\nStarting TopToolbar")
            #connect tooltip to fig
            mpld3.plugins.connect(fig, tooltip, TopToolbar())    
            print("\nSetting axes")
            
            #set tick marks as blank
            ax.axes.get_xaxis().set_ticks([])
            ax.axes.get_yaxis().set_ticks([])
            
            #set axis as blank
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)

            
        ax.legend(numpoints=1) #show legend with only one dot
        print("\ntrying to display")
        # mpld3.display() #show the plot
        mpld3.show() #show the plot

        # plt.show()
        # uncomment the below to export to html
        html = mpld3.fig_to_html(fig)
        # print(html)
        with open("bacon.html", "w") as f:
            f.writelines(html)
        print("bacon.html file created!")

#define custom toolbar location
class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}

