from elasticsearch import Elasticsearch
import re

class Elastic:
    
    def __init__(self, size=None, keywords= None):
        self.size = 1000
        self.keywords = ''

    def query(self):
        while True:
            try:
                self.keywords =  [input('What keywords do you want?: ').replace(',',' ').lower().strip()]
                if self.keywords == ['']:
                    break
            except ValueError:
                if len(self.keywords) != 0 and self.keywords[0] != '':
                    print("Not an integer!")
                    continue
                else:
                    print("Nothing typed. Exiting..")
                    break
            else:
                break 
        return self.keywords

    def queryElastic_name(self):
        es = Elasticsearch(['192.168.20.32:9200'])
        while True:
            keywords = self.query()
            if keywords == ['']:
                search_results = None
                return search_results
            search_results = es.search(index = 'cv', doc_type= 'txt', size=self.size,
                            body = {"_source": "name",
                                "query": {
                                "match":{"content": {"query": keywords[0], "analyzer": 'patterned_analyzer'}}
                                }
                            })
            if search_results["hits"]["total"] != 0 and len(keywords) != 0:
                print('Found {} hits!'.format(search_results["hits"]["total"]))
                break
            else:
                print("\nNo input given or 0 hits.. Try again: ")
                continue

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
        if search_results == None:
            return 'No input given! Exiting..'
        self.n = 0
        self.i = 0
        if search_results["hits"]["total"] == 0:
            print('No results found.. Try again!')
        else:
            while True:
                try:
                    self.n = int(input("Results to show: "))
                    if self.n > self.size:
                        print("Value too big.. Make it less than {}!".format(self.size))
                        continue
                except ValueError:
                    print("Not an integer!")
                    continue
                else:
                    break 
            while self.i < self.n and self.i < search_results["hits"]["total"]:
                print(self.i+1,
                    "| filename:",
                    search_results["hits"]["hits"][self.i]["_source"]["name"][:-4],
                    "| score:",
                    search_results["hits"]["hits"][self.i]["_score"])
                self.i += 1
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
            for self.i in range(5):
                print(i+1,
                    "| filename:",
                    search_results["hits"]["hits"][self.i]["_source"]["content"],
                    "| score:",
                    search_results["hits"]["hits"][self.i]["_score"])
                self.i += 1
    
    def show_content(self, filename):
        search_results = self.queryElastic_content(filename)
        # print('\n' + search_results["hits"]["hits"][0]["_source"]["content"])
        print()
        self.summary(search_results["hits"]["hits"][0]["_source"]["content"], filename)
        # print('\nExit!')

    def summary(self, corpus, filename, ):
        import summarizer
        import difflib
        from gensim.summarization.summarizer import summarize
        visited = []
        words = self.keywords[0].split()
        summarizer = summarizer.Summarizer()
        corpus_pro = summarizer.create_summary(corpus)
        text_list = corpus.split('\n')
        for sent in text_list:
            sent_pro = re.sub(r'[^A-Za-zÁ-ÿ#/+.0-9]+', ' ', sent)
            # sent_pro = re.sub(r'[\W+^#]+', ' ', sent)
            sent_list = sent_pro.split()
            sent_list = [item.lower() for item in sent_list]
            # print(sent_list)
            for word in sent_list:
                # if (word.lower() in words) and (sent not in visited):
                if difflib.get_close_matches(word, words) and (sent not in visited):
                    # print(difflib.get_close_matches(word, sent_list))
                    visited.append(sent)
                    break
        # print(corpus_pro)
        sentence_n = 5
        # rank = list(set(summarize(corpus_pro).split("\n")))
        rank = corpus_pro
        j = 0
        print('*'*100)
        print('Closed matched phrases of', filename)
        print('*'*100)

        for i, elem in enumerate(visited):
            print('\n ● ' + elem)   
            if i > 5:
                break
        print()

        print('*'*100)
        print('Summary of', filename)
        print('*'*100)

        while j <= sentence_n:
            if len(rank) <= j:
                break
            print('\n ● ' + rank[j])
            j += 1
        
        self.try_again()

    def try_again(self,):
        print()
        self.name()

if __name__ == "__main__":
    elastic = Elastic()
    elastic.name()