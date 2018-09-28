import glob

class Ingest():
    
    def __init__(self):
        self.folder = r"/home/emanuel/Desktop/CV"
        self.filenames = []
        self.folders = []
        
    def getTxts(self):
        # paths = glob.glob(self.folder + r'/*.pdf')
        self.txt_subfolders()
        for x in self.subfolders:
            if x.endswith('.txt'):
                self.filenames.append(x.split('/')[-1])
                self.folders.append("/".join(x.split('/')[:-1]))
        return self.filenames, self.folders
    
    def txt_subfolders(self):
        self.subfolders = glob.glob(self.folder + r"/*/text_files/*.txt", recursive=True)
        return self.subfolders

if __name__ == "__main__":
    ingest = Ingest()
    filenames, folders = ingest.getTxts()