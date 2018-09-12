#%%
from packages import Parser2txt, Paths

class Main():

    def __init__(self):
        # Parser.__init__(self)
        pass

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

    # parser = Parser2txt(cv_path)
    # lista = parser.docLists()
    
    gandalf = Paths(cv_path)
    wizard, bacon = gandalf.getPdfs()

    # parser.outputTxt()