import os
from ftplib import FTP
import json
import pandas as pd
import elastic
import subprocess


def elastic_insertion(file_path):
    with open(file_path) as f:
        file = f.readlines()
        filename = os.path.basename(f.name)
    json_line = file.pop(0)
    data = [float(line) for line in file]
    json_dict = json.loads(json_line)
    json_dict['data'] = [data]
    json_dict['Tags'] = [json_dict['Tags']]
    dataframe_dict = dict()
    dataframe_dict['filename'] = filename
    dataframe_dict['content'] = [json_dict]
    df = pd.DataFrame(dataframe_dict)
    try:
        elastic.bulk_indexing(df, 'guided_waves')
    except ConnectionError:
        subprocess.call('awakeEL.sh', shell=True)




