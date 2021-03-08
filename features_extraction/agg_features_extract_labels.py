from numpy.lib.function_base import extract
from numpy.lib.npyio import save
from numpy.matrixlib.defmatrix import matrix
import s3fs
import numpy as np
import re
import os
import argparse


def extract_labels(features_matrix, window_size, alpha=0.03):
    """alpha avoid noise"""
    labels = []
    for line in range(len(features_matrix)):
        current_price = features_matrix[line,1]
        time = features_matrix[line, 0]
        further_price = np.mean(features_matrix[line+1:line+window_size+1,1])
        porportion = further_price/current_price
        if porportion > 1+alpha:
            labels.append([time, 1])
        elif porportion < 1-alpha:
            labels.append([time,-1])
        else:
            labels.append([time,0])
    return np.array(labels, dtype=np.float32)


def save_arrays(fs, write_path, obj):
    with fs.open(write_path,'wb') as f:
        np.save(f, obj)


def agg_features_perday(files, args):
    pattern = re.compile("(?<=_)2022-[0-9]{2}-[0-9]{2}")
    date = re.search(pattern=pattern,string=files[0]).group()
    feature_matrix = np.load(files[0])
    cols = feature_matrix.shape[1]
    for file in files[1:]:
        current_date = re.search(pattern, file).group()
        if current_date != date:
            print(f"the previous date is {date}, current date is {current_date}")
            save_arrays(fs, os.path.join(args.s3_bucket, args.bucket_name, args.write_folder, f"features_{date}.npy"), feature_matrix)
            print(f"finish saving features of {date}")
            labels = extract_labels(feature_matrix[:,[0, args.mid_price_col]], args.window_size)
            print(f"start saving labels of {date}...")
            save_arrays(fs, os.path.join(args.s3_bucket, args.bucket_name, args.write_folder,f"labels_{date}.npy"),labels)
            print(f"finish saving labels of {date}...")
            date = current_date
            feature_matrix = np.array([]).reshape(0, cols)

        current_features = np.load(file)
        feature_matrix = np.concatenate((feature_matrix, current_features), axis=0)
    # The final result
    labels = extract_labels(feature_matrix[:,[0, args.mid_price_col]], args.window_size)
    save_arrays(fs, os.path.join(dir, f"features_{date}.npy"), feature_matrix)
    save_arrays(fs, os.path.join(args.s3_bucket, args.bucket_name, args.write_folder,f"labels_{date}.npy"),labels)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_name", default="b_02", type=str)
    parser.add_argument("--read_folder", default="features", type=str)
    parser.add_argument("--write_folder", default="agg_features_perday", type=str)
    parser.add_argument("--s3_bucket", default="s3://uob-miniproject", type=str)
    parser.add_argument("--window_size", default=10, type=int)
    parser.add_argument("--mid_price_col", default=7, type=int)

    
    args = parser.parse_args()

    fs = s3fs.S3FileSystem(anon=False)
    files = fs.ls(os.path.join(args.s3_bucket, args.bucket_name, args.read_folder))
    # files=['./data/features_2022-01-04_0.npy','data/features_2022-01-04_1.npy','data/features_2022-01-05_0.npy']
    agg_features_perday(files, args)




    


