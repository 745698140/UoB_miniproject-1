# coding: utf-8
'''
@filename:extract_features_h.py
@Createtime: 2021/02/22 16:22:52
@author: Haishuo Fang
@description: another possible extraction framework.
'''
from build_features import best_ask_price, average_midprice_financial_duration, best_bid_price
import json
import pandas as pd
from data_exploration import json_to_df, read_file
import time 
import multiprocessing
import numpy as np
from c_features import lob, lobs
import os

def get_features(json_data, num_features, time_window, batch_number):
    print(f"starting process {batch_number} files at process {os.getpid()}")
    feature_matrix = np.zeros((len(json_data), num_features))
    # Create multiprocessing pool
    tik = time.time()
    try:
        for i, entry in enumerate(json_data):
            # Get json for this lob
            if not entry['bid'] or not entry['ask']:
                continue
            this_lob = lob(entry)
            # Get groups of json given k
            if i >= time_window-1:
                group_lobs = lobs(json_data[(i-(time_window-1)):(i+1)])
            else:
                group_lobs = lobs(json_data[:i+1])
            
            # Calculate vals, this could be done in parallel
            feature_matrix[i][0] = this_lob.time
            feature_matrix[i][1] = this_lob.microprice()
            feature_matrix[i][2] = this_lob.total_quantity_all_quotes()
            feature_matrix[i][3] = group_lobs.average_midprice_financial_duration()
        
        tok = time.time()
        print(f'time taken for processing {batch_number} is {tok-tik} s')
        np.save('./data/features_extracted{batch_number}.npy', feature_matrix)
        # columns=['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration']
        # df = pd.DataFrame(feature_matrix,columns=columns)
        # df.to_csv(f'./data/test{batch_number}.csv')
        print(f"finish processing {batch_number}!")

    except Exception as error:
        print(error)
        return f"Error in batch {batch_number}, That is {error}"
        
if __name__ == "__main__":
    json_string = read_file('.','data/TstB02_2022-01-04LOBs.json')
    # json_string = read_file('.','data/test.json')
    json_data = json.loads(json_string)
    print('loaded json data')

    # json_string2 = read_file('.','data/TstB02_2022-01-04LOBs.json')
    # print("loaded json_string")
    # df = json_to_df(json_string=json_string)
    # df2 = json_to_df(json_string=json_string2)
    # print("convert to df")
    # tapes = pd.read_csv("data/TstB02_2022-01-04tapes.csv", header=None)

    batch_size = 10000
    pool = multiprocessing.Pool(3)
    data = [(json_data[i:i+batch_size], 4, 10, i//batch_size) for i in range(0,len(json_data[:100000]), batch_size)]
    results = pool.starmap_async(get_features, data)
    if results.get()[0]:
        print(results.get())
    pool.close()
    pool.join()
    

   
    


    
    