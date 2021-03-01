# coding: utf-8
'''
@filename:extract_features_h.py
@Createtime: 2021/02/22 16:22:52
@author: Haishuo Fang
@description: another possible extraction framework.
'''
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
    
    # Create multiprocessing pool
    # tik = time.time()
    try:
        feature_matrix = batch_features_extraction(time_window, len(json_data), json_data, num_features)
        if batch_number == 0:
            # calculate the first k data points less than time_window
            feature_matrix_init = batch_features_extraction(1, time_window-1, json_data, num_features)
            feature_matrix = np.concatenate((feature_matrix_init, feature_matrix), axis=0)

        # tok = time.time()
        # print(f'time taken for processing {batch_number} is {tok-tik} s')

        # np.save(f'./data/features_extracted{batch_number}.npy', feature_matrix)
        columns=['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration']
        df = pd.DataFrame(feature_matrix,columns=columns)
        df.to_csv(f'./data/test{batch_number}.csv')
        print(f"finish processing {batch_number}!")

    except Exception as error:
        print(error)
        return f"Error in batch {batch_number}, That is {error}"
        

def batch_features_extraction(time_window, end_index, json_data, num_features):
    feature_matrix = np.zeros((end_index-time_window+1, num_features))
    for i in range(time_window-1, end_index):
        # filter out Null bid and ask
        if not json_data[i]['bid'] or not json_data[i]['ask']:
            continue
        this_lob = lob(json_data[i])
        if time_window==1:
            group_lobs = lobs(json_data[:(i+1)])
        else:
            group_lobs = lobs(json_data[(i-(time_window-1)):(i+1)])
    
        # Calculate vals, this could be done in parallel
        index = i-(time_window-1)
        feature_matrix[index][0] = this_lob.time
        feature_matrix[index][1] = this_lob.microprice()
        feature_matrix[index][2] = this_lob.total_quantity_all_quotes()
        feature_matrix[index][3] = group_lobs.average_midprice_financial_duration()
    return feature_matrix


if __name__ == "__main__":
    json_string = read_file('.','data/TstB02_2022-01-04LOBs.json')
    # json_string = read_file('.','data/feature_testing.json')
    json_data = json.loads(json_string)
    print('loaded json data')

    # json_string2 = read_file('.','data/TstB02_2022-01-04LOBs.json')
    # print("loaded json_string")
    # df = json_to_df(json_string=json_string)
    # df2 = json_to_df(json_string=json_string2)
    # print("convert to df")
    # tapes = pd.read_csv("data/TstB02_2022-01-04tapes.csv", header=None)
    start = time.time()
    batch_size = 100000
    processes = 6
    window_size = 10
    number_features = 4
    pool = multiprocessing.Pool(processes=processes)

    # The first batch
    data = [(json_data[0:batch_size], number_features, window_size, 0)]
    # Remaining batch needs to add the previous k data points
    remain = [(json_data[i-window_size+1:i+batch_size], number_features, window_size, i//batch_size) for i in range(batch_size,len(json_data), batch_size)]
    data.extend(remain)
    results = pool.starmap_async(get_features, data)
    if results.get()[0]:
        print(results.get())
    pool.close()
    pool.join()

    print(f'consuming time{time.time()-start}')
    

   
    


    
    