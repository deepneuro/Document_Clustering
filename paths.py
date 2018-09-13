#%%
from packages import glob
class Paths():
    def __init__(self, folder, filenames=None, subfolders=None, folders=None):
        self.folder = folder
        self.filenames = filenames
        self.subfolders = subfolders
        self.folders = folders
        if self.filenames is None:
            self.filenames = []
        if self.folders is None:
            self.folders = []

    def loadClass(self):
        print("Loaded Paths class")

    def getPath(self):
        return self.folder

    def pdf_subfolders(self):
        self.subfolders = glob.glob(self.folder + r"/**/*.pdf", recursive=True)
        return self.subfolders

    def getPdfs(self):
        # paths = glob.glob(self.folder + r'/*.pdf')
        self.pdf_subfolders()
        for x in self.subfolders:
            if x.endswith('.pdf'):
                self.filenames.append(x.split('/')[-1])
                self.folders.append("/".join(x.split('/')[:-1]))
        return self.filenames, self.folders
    
    def makeFolder(self, directory):
        from packages import glob, os, errno
        try:
            os.makedirs(directory)
            print(directory, 'created!')
        except OSError as e:
            print('\nFolder', directory, 'exists!\n')
            if e.errno != errno.EEXIST:
                raise
        return self.folder + r'/outputTxt/'