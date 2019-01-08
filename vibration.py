import datetime
import time
from elasticsearch import Elasticsearch
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.offline import iplot, init_notebook_mode, plot

init_notebook_mode(connected=True)

es = Elasticsearch(['192.168.20.32:9200'])


class StreamGraph:

    def __init__(self, index, refresh_rate):
        self.index = index
        self.current_index = 0
        self.refresh_rate = refresh_rate
        self.ploted_data = list()
        self.ploted_dates = list()

    def generate_recent_dates(self, seconds=10, offset=7200):
        self.now = datetime.datetime.now()
        self.offset_time = self.now - datetime.timedelta(seconds=offset)
        self.initial_time = self.offset_time - datetime.timedelta(seconds=seconds)
        self.offset_time_str = self.offset_time.strftime('%y%m%d%H%M%S')
        self.initial_time_str = self.initial_time.strftime('%y%m%d%H%M%S')
        return [self.initial_time_str, self.offset_time_str], [self.initial_time, self.offset_time]

    def query_elastic(self):
        query_body = {"sort": {
            "file.date": {
                "order": "asc"
            }
        },
            "query": {
                "range": {
                    "file.date": {
                        "gte": int(self.initial_time_str),
                        "lt": int(self.offset_time_str)
                    }
                }
            }
        }

        number_hits = es.search(index=self.index,
                                doc_type='txt',
                                size=0,
                                body=query_body)['hits']['total']
        self.elastic_results = es.search(index=self.index,
                                    doc_type='txt',
                                    size=number_hits,
                                    body=query_body)
        return self.elastic_results

    def extract_fields(self, field):
        self.results_list = list()
        for results in self.elastic_results['hits']['hits']:
            self.results_list += results['_source']['file']['data'][0][field]
        return self.results_list

    def create_dates_list(self):
        self.delta = (self.offset_time - self.initial_time).seconds
        self.initial_time = self.initial_time - datetime.timedelta(microseconds=self.initial_time.microsecond)
        self.delta_per_tick = datetime.timedelta(seconds=self.delta / len(self.results_list))
        self.times_list = [self.initial_time + i * self.delta_per_tick for i in
                           range(len(self.results_list))]
        return self.times_list

    def refresh_all(self, field):
        self.generate_recent_dates()
        self.query_elastic()
        self.extract_fields(field)
        self.create_dates_list()

    def change_refresh_rate(self, refresh_rate):
        self.refresh_rate = refresh_rate
        self.list_len = len(self.results_list) / (self.refresh_rate*self.delta)

    def actualize_data(self, field):
        self.next_index = int(self.current_index + self.list_len)
       # print("next_index: ", self.next_index)
        if self.next_index < len(self.results_list):
            self.refreshed_data = self.results_list[self.current_index: self.next_index]
            self.refreshed_dates = self.times_list[self.current_index: self.next_index]

        else:
            self.next_query_index = int(self.next_index - len(self.results_list))
            #print("next_query_index (change query): ", self.next_query_index)
            self.next_index = int(len(self.results_list))
            #print("next_index (change query): ", self.next_index)
            self.refreshed_data = self.results_list[self.current_index: self.next_index]
            self.refreshed_dates = self.times_list[self.current_index: self.next_index]
            self.refresh_all(field)
            self.current_index = 0
            self.next_index = self.next_query_index
            #print("next_index (change query): ", self.next_index)
            self.refreshed_data += self.results_list[self.current_index: self.next_index]
            self.refreshed_dates += self.times_list[self.current_index: self.next_index]

        if len(self.ploted_data) > 10000:
            self.ploted_data = self.ploted_data[len(self.refreshed_data):] + self.refreshed_data
            self.ploted_dates = self.ploted_dates[len(self.refreshed_dates):] + self.refreshed_dates
        else:
            self.ploted_data += self.refreshed_data
            self.ploted_dates += self.refreshed_dates
        self.current_index = self.next_index
        #print(self.current_index)

    def create_stream(self, field):
        self.refresh_all(field)

        while True:
            timer = time.time()
            self.actualize_data(field)
            #s.write(dict(x=self.ploted_dates, y=self.ploted_data))
            time_passed = time.time()-timer
            data = Scatter(y=self.ploted_data, x=self.ploted_dates,)

            plot([data], fileopt='extend')
            if time_passed < self.refresh_rate:
                time.sleep(self.refresh_rate-time_passed)
            #print(self.refresh_rate-time_passed)
            #print(self.refreshed_data[0],self.refreshed_dates[0])


import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# Get stream id from stream id list
#py.sign_in('n1ur0', 'hfp660LsUY0RQPpDh2w6')
#stream_id = 'w2frl4t4hx'

# Make instance of stream id object
#stream_1 = dict(token=stream_id, maxpoints=10000)
#trace1 = go.Scatter(
#    x=[],
#    y=[],
#    mode='lines+markers',
#    stream=stream_1         # (!) embed stream id, 1 per trace
#)
#data = go.Data([trace1])
#layout = go.Layout(title='Time Series')
#fig = go.Figure(data=data, layout=layout)
#plot_url = py.plot(fig)
#s = py.Stream(stream_id)
#s.open()