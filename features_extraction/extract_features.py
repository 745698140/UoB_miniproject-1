# coding: utf-8
'''
@filename:extract_features_h.py
@Createtime: 2021/02/22 16:22:52
@author: Haishuo Fang
@description: another possible extraction framework.
'''
import json
import pandas as pd
import time 
import multiprocessing
import numpy as np
from all_features import lob, lobs
import os
import s3fs
import argparse
import re


def read_file(fs, dir, file_name):
    """read raw files"""
    with fs.open(os.path.join(dir, file_name), 'r', encoding='us-ascii') as f:
        string = f.read()
    return string


def get_features(json_data, num_features, time_window, batch_number, loblevel, date, write_path):
    print(f"starting process {batch_number} files at process {os.getpid()}")
    
    # Create multiprocessing pool
    # tik = time.time()
    try:
        feature_matrix = batch_features_extraction(time_window, len(json_data), json_data, num_features,loblevel=loblevel)
        if batch_number == 0:
            # calculate the first k data points less than time_window
            feature_matrix_init = batch_features_extraction(1, time_window-1, json_data, num_features, loblevel=loblevel)
            feature_matrix = np.concatenate((feature_matrix_init, feature_matrix), axis=0)

        # tok = time.time()
        # print(f'time taken for processing {batch_number} is {tok-tik} s')
        with fs.open(os.path.join(write_path,f'features_{date}_{batch_number}.npy'),'wb') as f:
            np.save(f, feature_matrix)
        
        # columns=['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration']
        # df = pd.DataFrame(feature_matrix,columns=columns)
        # df.to_csv(f'./data/test{batch_number}.csv')
        print(f"finish processing {date}_{batch_number}!")

    except Exception as error:
        raise error
        # return f"Error in batch {batch_number}, That is {error}"
        

def batch_features_extraction(time_window, end_index, json_data, num_features, loblevel):
    feature_matrix = np.zeros((end_index-time_window+1, num_features))
    lob_list = [lob(entry) for entry in json_data]

    for i in range(time_window-1, end_index):
        # filter out Null bid and ask
        # if not json_data[i]['bid'] or not json_data[i]['ask']:
            # continue
        this_lob = lob_list[i]

        if time_window==1:
            group_lobs = lobs(lob_list[:(i+1)])
        else:
            group_lobs = lobs(lob_list[(i-(time_window-1)):(i+1)])
    
        # Calculate vals, this could be done in parallel
        index = i-(time_window-1)
        feature_matrix[index][0] = this_lob.time
        feature_matrix[index][1] = this_lob.microprice()
        feature_matrix[index][2] = this_lob.total_quantity_all_quotes()
        feature_matrix[index][3] = this_lob.volume_imbalance()
        feature_matrix[index][4], feature_matrix[index][5] = this_lob.cumulative_sum_price_levels(loblevel)
        feature_matrix[index][6] = this_lob.mid_price_weighted_by_order_imbalance()
        feature_matrix[index][7] = this_lob.mid_price()
        
        feature_matrix[index][8] = group_lobs.average_midprice_financial_duration()
        feature_matrix[index][9] = group_lobs.realized_variance()
        feature_matrix[index][10] = group_lobs.positive_realized_semi_variance()
        feature_matrix[index][11] = group_lobs.negative_realized_semi_variance()

    
    return feature_matrix

def load_data_from_s3(fs, s3_bucket, start, end):
    files = fs.ls(s3_bucket)
    return files[start:end]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_index", type=int)
    parser.add_argument("--end_index", type=int)
    parser.add_argument("--batch_size", default=100000, type=int)
    parser.add_argument("--processors", default=8, type=int)
    parser.add_argument("--window_size", default=10, type=int)
    parser.add_argument("--loblevel", default=4, type=int)
    parser.add_argument("--subpath_s3bucket", default="b_02", type=str)
    
    args = parser.parse_args()
    pattern = re.compile("(?<=_)2022-[0-9]{2}-[0-9]{2}")
    fs = s3fs.S3FileSystem(anon=False)
    # json_string = read_file('.','data/TstB02_2022-01-04LOBs.json')
    s3_bucket = "s3://uob-miniproject"
    json_data_path = os.path.join(s3_bucket, args.subpath_s3bucket, 'json')
    write_path = os.path.join(s3_bucket, args.subpath_s3bucket, 'features')
    file_names = load_data_from_s3(fs, json_data_path, args.start_index, args.end_index)
    for file in file_names:
        if '.json' not in file:
            continue
        json_string = read_file(fs, '', file)
        json_data = json.loads(json_string)
        date = re.search(pattern, file).group()
        print('loaded json data')

        # json_string2 = read_file('.','data/TstB02_2022-01-04LOBs.json')
        # print("loaded json_string")
        # df = json_to_df(json_string=json_string)
        # df2 = json_to_df(json_string=json_string2)
        # print("convert to df")
        # tapes = pd.read_csv("data/TstB02_2022-01-04tapes.csv", header=None)
        start = time.time()
        batch_size = args.batch_size
        processes = args.processors
        window_size = args.window_size
        number_features = 12
        loblevel = args.loblevel
        pool = multiprocessing.Pool(processes=processes)

        # The first batch
        data = [(json_data[0:batch_size], number_features, window_size, 0, loblevel, date, write_path)]
        # Remaining batch needs to add the previous k data points
        remain = [(json_data[i-window_size+1:i+batch_size], number_features, window_size, i//batch_size, loblevel, date, write_path) for i in range(batch_size,len(json_data), batch_size)]
        data.extend(remain)
        results = pool.starmap_async(get_features, data)
        if results.get()[0]:
            print(results.get())
        pool.close()
        pool.join()

        print(f'consuming time{time.time()-start}')
