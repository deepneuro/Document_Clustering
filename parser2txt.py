#%%
from packages import PDFPage, PDFResourceManager, TextConverter, PDFPageInterpreter, io, LAParams
from paths import *

class Parser2txt():

    def __init__(self, folder, pdfName, filenames=None):
        #Main.__init__(self)
        self.folder = folder
        self.pdfName = pdfName
        #super().__init__(self, filenames)

    def loadClass(self):
        print("Loaded Parser class!")

    # get CV path
    def getMainPATH(self):
        return self.folder
    # get
    def getPATH(self):
        return self.pdfPATH

    def getFilePath(self):
        return self.folder + self.pdfName

    # Variable dumper if needed
    def pdf_var(self):
        # manager = PDFResourceManager()
        # codec = 'utf-8'
        pass

    def pdf2text(self, filename):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # fp = open(self.folder + self.pdfName, 'rb')
        fp = open(self.folder + "/" + filename, 'rb')
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
        paths = Paths(self.folder, self.pdfName)
        self.filenames = paths.getPdfs()
        for i, filename in enumerate(self.filenames):
            self.pdf2text(filename)
            # print(self.text)
            documents.append([filename])
            documents[i].append(self.text)
            txt.append(self.text)
            if i < 10: print('Doc Num:',i,' | Filename:', filename)
            else: print('Doc Num:',i,'| Filename:', filename)


        print("Pdf2Text completed!")
        return documents