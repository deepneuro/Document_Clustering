#%%
from packages import glob

class Paths():

    def __init__(self, folder, pdfName, filenames=None):
        self.folder = folder
        self.pdfName = pdfName
        self.filenames = filenames
        if self.filenames is None:
            self.filenames = []


    def loadClass(self):
        print("Loaded Paths class")

    def getPath(self):
        return self.folder

    def getPdfs(self):
        paths = glob.glob('/home/emanuel/Desktop/cvs/*.pdf')
        for x in paths:
            if x.endswith('.pdf'):
                self.filenames.append(x.split('/')[-1])
        return self.filenames


