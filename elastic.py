from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import re

# Defining the server of ElasticSearch
es = Elasticsearch(['192.168.20.32:9200'])


def define_index(index_name):
    """
    Function to create an index in the ElasticSearch database. It comes with
    the necessary mapping to tokenize properly the "content" field inside the
    new index.
    :param index_name: The name of the index to be created
    :return: Nothing, creates index in ElasticSearch
    """
    body = {"settings": {
                         "analysis": {
                                      "analyzer": {
                                                   "patterned_analyzer": {
                                                                          "type": "pattern",
                                                                          "pattern": "[^A-Za-zÁ-ÿ#+0-9]+",
                                                                          "filter": [
                                                                                     "lowercase"
                                                                                    ]
                                                                         }
                                                   }
                                      }
                         },
            "mappings": {
                         "txt": {
                                 "properties": {
                                                "text": {
                                                            "type": "text",
                                                            "analyzer": "patterned_analyzer"
                                                           }
                                               }
                                }
                        }
            }

    es.indices.create(index=index_name, ignore=400, body=body)


def bulk_indexing(documents_dataframe, index_name):
    """
    Given a DataFrame with documents, ingests them to the given index
    :param documents_dataframe: pandas.DataFrame with a column with the name of
    the file (Note that the mappings are done in a way that it's assumed that
    the text file is in a column named "content")
    :param index_name: string, Name of the index where the documents will be
    indexed
    :return: Nothing, documents will be indexed
    """
    column_names = documents_dataframe.columns

    def generate_data():

        for value in documents_dataframe.values:
            body = dict([(column_name, value[index])
                        for index, column_name in enumerate(column_names)])
            body.update({"_index": index_name,
                         "_type": 'txt'})
            yield body

    bulk(es, generate_data())


def query_elastic_by_keywords(keywords, index, max_size=10):
    """
    Query ElasticSearch index with desired keywords.
    :param keywords: str, keywords to be searched
    :param max_size: int, maximum number of returns
    :return: A JSON with results
    """

    # JSON of the query
    query_body = {"query": {
                            "match_phrase": {
                                             "text": {
                                                         "query": keywords,
                                                         "analyzer": 'patterned_analyzer'
                                                        }
                                             }
                            }
                  }

    elastic_results = es.search(index=index,
                                doc_type='txt',
                                size=max_size,
                                body=query_body)
    return elastic_results


def query_elastic_by_filename(filename):
    """
    Query ElasticSearch index with desired filename.
    :param filename: str, filename to be found
    :return: A JSON with results
    """

    # JSON of the query
    query_body = {"query": {
                            "match_phrase": {
                                             "name": filename
                                     }
                            }
                  }

    elastic_results = es.search(index='cv',
                                doc_type='txt',
                                size=1,
                                body=query_body)

    return elastic_results


def return_files_by_field(elastic_results, return_field, number_displayed_results=10):
    """
    Given a ElasticSearch query result, returns the wanted field.
    :param elastic_results:Dictionary, ElasticSearch JSON result
    :param return_field: string, field to be presented
    :param number_displayed_results: int, number of max results to be displayed
    :return: List of the content of the fields in the results
    """
    number_results = len(elastic_results["hits"]["hits"])

    # define the number of documents that will be displayed
    if number_displayed_results > number_results:
        number_iterations = elastic_results["hits"]["total"]
    else:
        number_iterations = number_displayed_results

    # define the output taking into account the number of results
    if number_results == 0:
        return ['No results']

    else:

        # score is stored in a different level of the dictionary
        if return_field == "score":
            field_list = [elastic_results['hits']['hits'][doc_number]['_score']
                          for doc_number in range(number_iterations)]

        else:
            field_list = [elastic_results['hits']['hits'][doc_number]['_source'][return_field]
                          for doc_number in range(number_iterations)]

        return field_list

