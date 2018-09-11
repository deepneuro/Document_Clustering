#%%
from packages import *

class Main():
    
    def __init__(self):
        # self.x = x
        pass

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
    
    PATH = "/home/emanuel/Desktop/cvs/Emanuel Oliveira"
    pdfName = "CV_EmanuelOliveira_pt.pdf"




    parser = Parser(PATH, pdfName)
    print(parser.getMainPATH())
    print(parser.getFilePath())


    paths = Paths(PATH, pdfName)
    print(paths.getPdfs())