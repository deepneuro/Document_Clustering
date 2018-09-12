#%%
import sys
path = "/home/emanuel/Desktop/Doc_Clustering/Document_Clustering"
# path = "C:\\Users\\Emanuel\\Desktop\\DocClu\\Document_Clustering\\"

if path not in sys.path:
    print("added packages to $PYTHONPATH")
    sys.path.insert(0, path)
#%%
from packages import Parser2txt

class Main():

    def __init__(self):
        # self.x = x
        # Parser.__init__(self)
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
    print("Loaded main class\n")
    
    cv_path = r"/Users/emanuel/Desktop/Document_Clustering"
    #cv_path = r"C:\Users\sergiojesus\Desktop\Coisas da Alvita\CV\4-Abril_14"

    parser = Parser2txt(cv_path)
    # print(parser.getMainPATH())
    # print(parser.getFilePath())


    lista = parser.docLists()
    # print(lista)
    
    # gandalf = Paths(cv_path)
    # lista, bacon = gandalf.getPdfs()

    # for x in bacon:
    #     print(x)
    # print(len(lista))
    # parser.outputTxt()