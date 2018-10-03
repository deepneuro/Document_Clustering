from elasticsearch import Elasticsearch
import re

# Defining the server of ElasticSearch
es = Elasticsearch(['192.168.20.32:9200'])


def query_elastic_by_keywords(keywords, max_size=100):
    """

    :param keywords:
    :param max_size:
    :return:
    """

    # JSON of the query
    query_body = {"_source": "name",
                  "query": {
                            "match_phrase": {
                                             "txt": {
                                                         "query": keywords,
                                                         "analyzer": 'patterned_analyzer'
                                                        }
                                             }
                            }
                  }

    search_results = es.search(index='cv',
                               doc_type='txt',
                               size=max_size,
                               body=query_body)
    return search_results


def query_elastic_by_filename(filename):
    """

    :param filename:
    :return:
    """

    # JSON of the query
    query_body = {"_source": "name",
                  "query": {
                            "match": {
                                      "name": filename
                                     }
                            }
                  }

    search_results = es.search(index='cv',
                               doc_type='txt',
                               size=1,
                               body=query_body)

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
    visited = []
    words = self.keywords[0].split()
    summarizer = summarizer.Summarizer()
    corpus_pro = summarizer.create_summary(corpus)
    text_list = corpus.split('\n')
    for sent in text_list:
        sent_pro = re.sub(r'[^A-Za-zÁ-ÿ^#+]+', ' ', sent)
        # sent_pro = re.sub(r'[\W+^#]+', ' ', sent)
        sent_list = sent_pro.split()
        for word in sent_list:
            if (word.lower() in words) and (sent not in visited):
                visited.append(sent)
                break
    # print(corpus_pro)
    sentence_n = 5
    # rank = list(set(summarize(corpus_pro).split("\n")))
    rank = corpus_pro
    j = 0
    print('*'*100)
    print('Matched Phrases of', filename)
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
        print('\n ● ' + rank[j])
        j += 1
