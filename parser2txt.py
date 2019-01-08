#%%
from packages import PDFPage, PDFResourceManager, TextConverter, PDFPageInterpreter, io, LAParams, detect_langs, detect
from paths import *
import pickle
import time
import pandas as pd

class Parser2txt(Paths):

    def __init__(self, folder, filenames=None, folders=None, errors=None):
        #Main.__init__(self)
        super().__init__(self)
        self.folder = folder
        self.errors = errors
        if self.errors == None:
            self.errors = []

    def loadClass(self):
        print("Loaded Parser class!")

    def saveObjs(self):
        with open('Doc_objs.pkl', 'wb') as f:
            pickle.dump([self.documents], f)
        print('Doc objects saved!')

    def loadObjs(self):
        with open('Doc_objs.pkl', 'rb') as f:
            self.documents = pickle.load(f)
        print('Doc objects loaded!')
        return self.documents

    def getNumFiles(self):
        return len(self.filenames)

    def getFilename(self, i):
        return self.documents[i]

    def getFilePath(self, filename, i):
        return self.folders[i] + "/" + filename

    def getListText(self):
        return list(self.text)

    def getListSize(self, x):
        return len(x)

    def langDetector(self,i=0):
        if self.documents and len(self.documents) != 0:
            try:
                return detect(self.documents[i][1])
            except:
                print("ERROR AT FILE:", self.documents[i][0])
                self.errors.append(self.documents[i][0])
        else:
            try:
                return detect(self.text)
            except:
                self.errors.append(self.text)

    def langDetector_tokens(self, text):
        try:
            return detect(text)
        except:
            self.errors.append(text)

    # def writeErrors(self):
    #     with open('Errors.txt', 'a') as f:
    #         f.writelines(self.errors)

    def pdf2text(self, filename, i):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # fp = open(self.folder + self.pdfName, 'rb')
        fp = open(self.getFilePath(filename, i), 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="",caching=True, check_extractable=True):
            interpreter.process_page(page)

        self.text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return self.text

    def openTxt(self, filename, i):
        with open(self.getFilePath(filename, i), 'r') as f:
            lista_corpus = f.readlines()
            self.text = ''.join(lista_corpus)
        return self.text

    def docLists(self):
        self.documents = []
        self.txtOnly = []
        if len(self.filenames) == 0:
            self.filenames, self.folders = self.getPdfs()
        for i, filename in enumerate(self.filenames):
            self.pdf2text(filename, i)
            # print(self.text)
            self.documents.append([filename])
            self.documents[i].append(self.text)
            self.txtOnly.append(self.text)
            print("document language:", self.langDetector(i))
            if i < 10: print('Doc Num:',i,' | Filename:', filename,)
            else: print('Doc Num:',i,'| Filename:', filename)
        return self.documents, self.txtOnly

    def docTxtLists(self):
        self.documents = []
        self.txtOnly = []
        if len(self.filenames) == 0:
            # self.filenames, self.folders = self.getPdfs()
            self.filenames, self.folders = self.getTxts()
        for i, filename in enumerate(self.filenames):
            # self.pdf2text(filename, i)
            self.openTxt(filename, i)
            self.documents.append([filename])
            self.documents[i].append(self.text)
            self.txtOnly.append(self.text)
            print("document language:", self.langDetector(i))
            if i < 10: print('Doc Num:',i,' | Filename:', filename,)
            else: print('Doc Num:',i,'| Filename:', filename)
            # break
        data = { 'filename': self.documents, 'txt': self.textOnly }
        df = pd.DataFrame(data, columns=["filename", "txt"])
        df.to_csv(self.folder + "/data.csv", sep=",")
        return self.documents, self.txtOnly

    def getCSVData(self):
        df = pd.read_csv(self.folder + "/data.csv")
        self.documents = df.filenames
        self.textOnly = df.text
        return df

    def outputTxt(self):
        self.txt_paths = []
        self.txt_filenames = []

        outFolder = self.makeFolder(self.folder + r'/outputTxt')
        self.filenames, _ = self.getPdfs()

        for i, filename in enumerate(self.filenames):
            inTime = time.time()
            self.pdf2text(filename, i)
            f_out = open(outFolder + filename[:-4] + '.txt', 'w')
            # f_out = open(self.getFilePath(filename, i)[:-4] + '.txt', 'w')
            f_out.write(self.text)
            f_out.close()
            # print("Doc Num:",i ,'| Written to:', self.getFilePath(filename, i)[:-4] + '.txt','\n')
            self.txt_paths.append(outFolder + filename[:-4] + '.txt')
            self.txt_filenames.append(str(outFolder + filename[:-4] + '.txt').split('/')[-1])
            outTime = time.time()
            print("Time:", round(outTime - inTime,1) ,"sec | Doc Num:",i ,'| Written to:', outFolder + filename[:-4] + '.txt','\n')

    def dump_txtPaths(self):
        from sklearn.externals import joblib
        joblib.dump([self.txt_paths,self.txt_filenames], 'doc_txtPaths.pkl')
        print("Txt filenames and paths saved!")

    def load_txtPaths(self):
        from sklearn.externals import joblib
        self.txt_paths,self.txt_filenames = joblib.load('doc_txtPaths.pkl')
        return self.txt_filenames,self.txt_paths


