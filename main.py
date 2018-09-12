#%%
import sys

#path = "/home/emanuel/Desktop/Doc_Clustering/Document_Clustering"
path = "C:\\Users\\Emanuel\\Desktop\\DocClu\\Document_Clustering\\"

if path not in sys.path:
    print("added packages to $PYTHONPATH")
    sys.path.insert(0, path)
sys.path
#%%
#from packages import *
class Main():

    def __init__(self):
        # self.x = x
        Parser.__init__(self)

    # def getTestA(self):
    #     print(self.a)

    # def getTestX(self):
    #     print(self.x)

if __name__ == "__main__":
    """
    INFO:
    - detail each function!
    - detail each function!
    - detail each function!
    - detail each function!
    """
    print("Loaded main class")

    path = r"C:\Users\Emanuel\Desktop\DocClu\CV"
    pdfName = r"\CV_EmanuelLimaOliveira_pt.pdf"

    parser = Parser(path, pdfName)
    print(parser.getMainPATH())
    print(parser.getFilePath())
    print(parser.pdf2text())

    paths = Paths(PATH, pdfName)
    print(paths.getPdfs())
