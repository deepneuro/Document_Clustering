#%%
from packages import PDFPage, PDFResourceManager, TextConverter, PDFPageInterpreter, io, LAParams
from paths import *

class Parser2txt(Paths):

    def __init__(self, folder, pdfName, filenames=None, folders=None):
        #Main.__init__(self)
        super().__init__(folder, pdfName, filenames, folders)
        self.folder = folder
        self.pdfName = pdfName

    def loadClass(self):
        print("Loaded Parser class!")

    # get CV pathS
    def getMainPATH(self):
        return self.folder
    # get
    def getPATH(self):
        return self.pdfPATH

    def getFilePath(self):
        return self.folder + self.pdfName

    def getNumFiles(self):
        return len(self.filenames)

    def getFilePath(self, filename, i):
        return self.folders[i] + "/" + filename

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

    def txtFiles(self):
        documents = []
        txt = []
        self.filenames, self.folders = self.getPdfs()
        for i, filename in enumerate(self.filenames):
            self.pdf2text(filename, i)
            # print(self.text)
            documents.append([filename])
            documents[i].append(self.text)
            txt.append(self.text)
            if i < 10: print('Doc Num:',i,' | Filename:', filename)
            else: print('Doc Num:',i,'| Filename:', filename)
        print("Pdf2List completed!")
        return documents

    def outputTxt(self):
        self.makeFolder(self.folder + r'/outputTxt')
        self.filenames, self.folders = self.getPdfs()

        for i, filename in enumerate(self.filenames):
            self.pdf2text(filename, i)
            f_out = open(self.getFilePath(filename, i)[:-4] + '.txt', 'w')

            # write using...
            f_out.write(self.text)

            f_out.close()
            print(self.getFilePath(filename, i)[:-4] + '.txt')
            break
        pass

        
    