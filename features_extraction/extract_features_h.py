# coding: utf-8
'''
@filename:extract_features_h.py
@Createtime: 2021/02/22 16:22:52
@author: Haishuo Fang
@description: another possible extraction framework.
'''
from build_features import best_ask_price, average_midprice_financial_duration, best_bid_price
import json
from typing import NamedTuple
from build_features import cumulative_sum_price_levels
import pandas as pd
from data_exploration import json_to_df, read_file
import time 
from c_features import lob, lobs

if __name__ == "__main__":
    json_string = read_file('.','feature_testing.json')
    df = json_to_df(json_string=json_string)
    # df['test'] = df.apply(lambda x: cumulative_sum_price_levels(x['ask'], x['bid'], 10), axis=1)

    start =  time.time()
    df['best_ask_prices'] = df['ask'].apply(lambda x: best_ask_price(x))
    df['best_bid_prices'] = df['bid'].apply(lambda x: best_bid_price(x))
    # average midprice_financial duration
    df['spread'] = df['best_ask_prices'] - df['best_bid_prices']
    df['time_cumsum'] = df['time'].cumsum()
    df['spread'] = df['spread'].cumsum()
    df['mdf'] = df['time_cumsum'] / df['spread']
    df['avg_midprice_fd'] = df['mdf'].rolling(10, min_periods=1).mean()
    print("dataframe time is", time.time() - start)
    # print(df['mdf'])
    # print(df['spread'])
    print(df['avg_midprice_fd'])
    # print(df['time_cumsum'])

####comapre#####
    j_son = json.loads(json_string)
    k = 10
    a = []
    start = time.time()
    for i, x in enumerate(j_son):
        # Get json for this lob
        this_lob = lob(x)
        # Get groups of json given k
        if i >= k-1:
            group_lobs = lobs(j_son[(i-(k-1)):(i+1)])
        else:
            group_lobs = lobs(j_son[:i+1])
        
        # Calculate vals, this could be done in parallel
        a.append(group_lobs.average_midprice_financial_duration())
    print("json loop time is", time.time()-start)

   
    


    
    