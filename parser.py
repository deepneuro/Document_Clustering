#%%
from packages import PDFResourceManager, TextConverter, PDFPageInterpreter, io, LAParams

class Parser():

    def __init__(self, folder, pdfName):
        #Main.__init__(self)
        self.folder = folder
        self.pdfName = pdfName

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

    def pdf2text(self):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(self.folder + self.pdfName, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="",caching=True, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text


Parser(None,None).loadClass()
# Parser("s", "ws").pdf2text()
