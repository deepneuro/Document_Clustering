#%%
# from packages import Parser2txt, Paths, Pre_processing, TextProcessing, Clustering, Plot
import parser2txt, paths, pre_processing, text_processing, clustering, plot

# class Main():

#     def __init__(self):
#         # Parser.__init__(self)
#         pass

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
    # cv_path = r"/home/emanuel/Desktop/cvs"
    cv_path = r"/home/emanuel/Desktop/CV"


    
    # cv_path = r"C:\Users\sergiojesus\DWesktop\Coisas da Alvita\CV\4-Abril_14"


    # filenames, pathss = parser.load_txtPaths()
    # parser.outputTxt()


    def test1():
        parser = parser2txt.Parser2txt(cv_path)
        # documents, _ = parser.docLists()
        documents, _ = parser.docTxtLists()
        return documents
        # parser.saveObjs()

    def test2(documents):
        # documents = parser.loadObjs()
        pre = pre_processing.Pre_processing(documents)
        pre.text_process(stem=False, lemma=True)
        pre.saveObjs()

    def test3():
        x = text_processing.TextProcessing(cv_path)
        x.corpus()
        x.saveTFIDF()

    def test4(): # Clusters = 20
        y = clustering.Clustering(cv_path)
        y.top_terms()

    def test5():
        graph = plot.Plot(cv_path)
        graph.buildGraph()

    def test6():
        graph = plot.Plot(cv_path)
        graph.buildGraph2()
    
    # pre.preparation()
    # print(pre.getTokenized())

    # pre = Pre_processing()
    # a, b, c = pre.loadObjs()
    
    # docs = test1()
    # test2(docs)
    # test3()
    test4()
    # test5()
    # test6()