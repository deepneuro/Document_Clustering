#%%
from packages import Parser2txt, Paths, Pre_processing

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
    
    # cv_path = r"/Users/emanuel/Desktop/Document_Clustering"
    cv_path = r"/home/emanuel/Desktop/cvs"
    
    # cv_path = r"C:\Users\sergiojesus\DWesktop\Coisas da Alvita\CV\4-Abril_14"

    parser = Parser2txt(cv_path)
    # lista = parser.docLists()
    
    # gandalf = Paths(cv_path)
    # wizard, bacon = gandalf.getPdfs()

    # parser.outputTxt()


    # documents = parser.docLists()
    # pre = Pre_processing(documents)
    pre = Pre_processing()

    # pre.preparation()
    # pre.text_process()
    # pre.saveObjs()
    # print(pre.getTokenized())
    # a, b = pre.loadObjs()