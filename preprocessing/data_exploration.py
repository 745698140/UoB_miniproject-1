from parse_raw_lob import process_file
import json
import os
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import gamma
from datetime import datetime, timedelta
import h5py
import re
from time import time
import seaborn as sns
import matplotlib.pyplot as plt


def realized_quantity(fun, index):
    """Applies the function 'fun' to each day separately"""
    return intraday_returns.groupby(pd.Grouper(freq="1d")).apply(fun)[index]

def convert_datetime(datestr,x):
    """convert seconds to datetime"""
    start = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S.%f")
    return start + timedelta(seconds=x)

def read_file(dir, file_name):
    """read raw files"""
    with open(os.path.join(dir, file_name), 'r', encoding='us-ascii') as f:
        string = f.read()
    return string

def write_file(dir, file_name, obj):
    """write json files"""
    with open(os.path.join(dir, file_name[:-4]+'.json'), 'w', encoding='us-ascii') as f:
        f.write(obj)

def json_to_df(json_string):
    """convert json to dataframe"""
    return pd.read_json(json_string, orient='records')


if __name__ == "__main__":
    folder_dir = "./data"
    file_name = "TstB02_2022-01-04LOBs.json"
    pattern = re.compile("(?<=_)2022-[0-9]{2}-[0-9]{2}")
    
    # file_working = read_file(folder_dir, file)
    # json_data = process_file(file_working)
    # write_file(folder_dir, file, json_data)
    # exit()

    # datetime
    # json_data = read_file(folder_dir, file_name)
    # df = json_to_df(json_data)
    
    # date = re.search(pattern,file_name).group()+" 08:00:00.0"
    # start = time()
    # df['date'] = df['time'].apply(lambda x: convert_datetime(date, x))
    # print(time()-start)
    # print(df.head(100))
    # df.to_hdf('./data/test.h5', 'data')

# plot transaction prices and trending
    tapes = pd.read_csv("./data/TstB02_2022-01-04tapes.csv", header=None)
    plt.figure(figsize=(8,8))
    sns.lineplot(x=2,y=3, data=tapes)
    plt.xlabel("transaction")
    plt.ylabel("price")
    plt.savefig('./data/2022-01-24-transactionprice')
    plt.show()
    
    
