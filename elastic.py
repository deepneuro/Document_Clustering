from elasticsearch import Elasticsearch

class Elastic:
    
    def __init__(self, size=None):
        self.size = 1000
    
    def query(self):
        while True:
            try:
                keywords =  [input('What keywords do you want?: ').replace(',','')]
            except ValueError:
                print("Not an integer!")
                continue
            else:
                break 
        return keywords

    def queryElastic_name(self):
        es = Elasticsearch(['192.168.20.32:9200'])
        while True:
            keywords = self.query()
            search_results = es.search(index = 'cv', doc_type= 'txt', size=self.size,
                            body = {"_source": "name",
                                "query": {
                                "match":{"content": keywords[0]},
                                }
                            })
            if search_results["hits"]["total"] != 0: break
            else: 
                print("\nNo input given.. Try again: ")
                continue

        print('Found {} hits!'.format(search_results["hits"]["total"]))

        return search_results

    def queryElastic_content(self, filename):
        es = Elasticsearch(['192.168.20.32:9200'])
        search_results = es.search(index = 'cv', doc_type= 'txt', size=1,
                        body = {"_source": "content",
                            "query": {
                                "match":{"name": filename},
                            }
                        })          
        return search_results

    
    def name(self):
        search_results = self.queryElastic_name()
        n = 0
        i = 0
        if search_results["hits"]["total"] == 0:
            print('No results found.. Try again!')
        else:
            while True:
                try:
                    n = int(input("Results to show: "))
                    if n > self.size:
                        print("Value too big.. Make it less than {}!".format(self.size))
                        continue
                except ValueError:
                    print("Not an integer!")
                    continue
                else:
                    break 
            while i < n and i < search_results["hits"]["total"]:
                print(i+1,
                    "| filename:",
                    search_results["hits"]["hits"][i]["_source"]["name"][:-4],
                    "| score:",
                    search_results["hits"]["hits"][i]["_score"])
                i += 1
        x = input("\nWant to see a summary? Press 'id_number' to show or 'no' to exit: ")
        if x.lower() != 'no' and x.lower() != '':
            filename = search_results["hits"]["hits"][int(x)-1]["_source"]["name"]
            self.show_content(filename)
        else: print('Exit!')

    def content(self):
        search_results = self.queryElastic_content()
        if search_results["hits"]["total"] == 0:
            print('No results found.. Try again!')
        else:
            for i in range(5):
                print(i+1,
                    "| filename:",
                    search_results["hits"]["hits"][i]["_source"]["content"],
                    "| score:",
                    search_results["hits"]["hits"][i]["_score"])
                i += 1
    
    def show_content(self, filename):
        search_results = self.queryElastic_content(filename)
        # print('\n' + search_results["hits"]["hits"][0]["_source"]["content"])
        print()
        self.summary(search_results["hits"]["hits"][0]["_source"]["content"], filename)
        print('\nExit!')

    def summary(self, corpus, filename):
        import summarizer
        from gensim.summarization.summarizer import summarize
        summarizer = summarizer.Summarizer()
        corpus_pro = summarizer.create_summary(corpus)
        # print(corpus_pro)
        sentence_n = 5
        # rank = list(set(summarize(corpus_pro).split("\n")))
        rank = corpus_pro
        j = 0
        print('*'*50)
        print('Summary of', filename)
        print('*'*50)
        while j <= sentence_n:
            print('\n ● '+rank[j])
            j += 1

if __name__ == "__main__":
    elastic = Elastic()
    elastic.name()