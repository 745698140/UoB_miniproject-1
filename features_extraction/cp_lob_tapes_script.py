import s3fs
import argparse
import os
import csv
import numpy as np
import pandas as pd

def save_arrays(fs, write_path, obj):
    with fs.open(write_path,'wb') as f:
        np.save(f, obj)

def get_the_time_in_tapes(files, args, time_set):
    for file in files:
        date = file[-19:-9]
        print(file)
        try:
            with fs.open(file, 'rb') as f:
                obj = pd.read_csv(f, names = ['Date', 'loc', 'time', 'price', 'pool_id', 'type', 'time2', 'price2', 'qty', 'praty1', 'party2'])
                time_list = list(obj['time'])
                for time in time_list:
                    time_set.add(date + '-' + str(time))
        except:
            continue
        
# add the label to find the changes caused by the transaction data
def add_compare_feature(files, args, time_set):
    for file in files[1:]:
        if 'label' in file:
            continue
        date = file[-14:-4]
        print(file)
        print(date)
        with fs.open(file, 'rb') as f:
            obj = np.load(f)
            temp = np.zeros((len(obj), 1))
            for i in range(len(obj)):
                time = date + '-' + str(obj[i][0])
                if time in time_set:
                    temp[i][0] = 1
            obj = np.hstack((obj,temp))
            save_arrays(fs, os.path.join(args.s3_bucket, args.bucket_name, args.write_folder, f"cp_features_{date}.npy"), obj)
            
            
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_name", default="b_02", type=str)
    parser.add_argument("--read_folder", default="features", type=str)
    parser.add_argument("--write_folder", default="agg_features_perday", type=str)
    parser.add_argument("--s3_bucket", default="s3://uob-miniproject", type=str)
    parser.add_argument("--window_size", default=10, type=int)
    parser.add_argument("--mid_price_col", default=7, type=int)
    parser.add_argument("--tapes_folder", default="raw/tapes", type=str)

    args = parser.parse_args()

    fs = s3fs.S3FileSystem(anon=False)
    tapes_files = fs.ls(os.path.join(args.s3_bucket, args.bucket_name, args.tapes_folder))
    feature_files = fs.ls(os.path.join(args.s3_bucket, args.bucket_name, args.write_folder))
    
    time_set = set()
    get_the_time_in_tapes(tapes_files, args, time_set)

    add_compare_feature(feature_files, args, time_set)
    


    

