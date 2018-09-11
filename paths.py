#%%
from packages import glob

class Paths():

    def __init__(self, folder, pdfName):
        self.folder = folder
        self.pdfName = pdfName
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


