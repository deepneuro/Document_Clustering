#%%
from packages import PDFPage, PDFResourceManager, TextConverter, PDFPageInterpreter, io, LAParams, detect_langs, detect
from paths import *

class Parser2txt(Paths):

    def __init__(self, folder, filenames=None, folders=None):
        #Main.__init__(self)
        super().__init__(self)
        self.folder = folder

    def loadClass(self):
        print("Loaded Parser class!")

    def getNumFiles(self):
        return len(self.filenames)

    def getFilePath(self, filename, i):
        return self.folders[i] + "/" + filename

    def getListText(self):
        return list(self.text)

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

    def docLists(self):
        self.documents = []
        txt = []
        self.filenames, self.folders = self.getPdfs()
        for i, filename in enumerate(self.filenames):
            self.pdf2text(filename, i)
            # print(self.text)
            self.documents.append([filename])
            self.documents[i].append(self.text)
            txt.append(self.text)
            print("document language:", self.langDetector(i))
            if i < 10: print('Doc Num:',i,' | Filename:', filename,)
            else: print('Doc Num:',i,'| Filename:', filename)
        print("Pdf2List completed!")
        return self.documents

    def outputTxt(self):
        outFolder = self.makeFolder(self.folder + r'/outputTxt')
        self.filenames, _ = self.getPdfs()

        for i, filename in enumerate(self.filenames):
            self.pdf2text(filename, i)
            f_out = open(outFolder + filename[:-4] + '.txt', 'w')
            # f_out = open(self.getFilePath(filename, i)[:-4] + '.txt', 'w')
            f_out.write(self.text)
            f_out.close()
            print("Doc Num:",i ,'| Written to:', self.getFilePath(filename, i)[:-4] + '.txt','\n')
            break
        pass

    def langDetector(self,i):
        return detect(self.documents[i][1])

        
    