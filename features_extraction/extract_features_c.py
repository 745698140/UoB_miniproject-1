import pandas as pd
import numpy as np
from c_features import lob, lobs
import json
import time
import multiprocessing as mp
import os

def extract_features(file_path) -> None:
    print(f'Extracting features from {file_path}')
    tik = time.time()
    with open(file_path) as json_file:
        j_son = json.load(json_file)

    # Define featuers for matrix, no k prev lobs
    features = ['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration']
    k = 10
    # Init feature matrix
    feature_matrix = np.zeros((len(j_son), len(features)))
    lob_list = [lob(x) for x in j_son]

    for i, this_lob in enumerate(lob_list):
        # Get groups of json given k
        if i >= k-1:
            group_lobs = lobs(lob_list[(i-(k-1)):(i+1)])
        else:
            group_lobs = lobs(lob_list[:i+1])
        
        feature_matrix[i][0] = this_lob.time
        feature_matrix[i][1] = this_lob.microprice()
        feature_matrix[i][2] = this_lob.total_quantity_all_quotes()
        feature_matrix[i][3] = group_lobs.average_midprice_financial_duration()
    
    tok = time.time()
    print(f'Feature extraction took {tok-tik} seconds ')
    
    # Add to df, print head
    df = pd.DataFrame(feature_matrix,columns=features).dropna(axis=0)
    print(df.head())
    df.to_csv(file_path[:-4]+'csv', index=False)
    print(f'Dumped to .csv')

if __name__ == "__main__":
    print(f'Number of cpu: {mp.cpu_count()}')
    dir = './'
    files = os.listdir(dir)
    json_files = [file for file in files if file.endswith('.json')]
    
    start_time = time.time()
    
    # Process each file on each cpu
    processes = []
    for i, file in enumerate(json_files):
        file_loc = dir+file
        p = mp.Process(target=extract_features, args = (file_loc,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f'Completed in {time.time()-start_time}')

