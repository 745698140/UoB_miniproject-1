import pandas as pd
import numpy as np
import multiprocessing as mp
from c_features import lob, lobs
import json
import time

if __name__ == "__main__":
    
    with open('./feature_testing.json') as json_file:
        j_son = json.load(json_file)
    
    # Define no of featuers for matrix
    num_features = 4
    # Define number of previous lobs
    k = 10
    # Init feature matrix
    feature_matrix = np.zeros((len(j_son), num_features))
    # Create multiprocessing pool
    tik = time.time()

    for i, x in enumerate(j_son):
        # Get json for this lob
        this_lob = lob(x)
        # Get groups of json given k
        if i >= k-1:
            group_lobs = lobs(j_son[(i-(k-1)):(i+1)])
        else:
            group_lobs = lobs(j_son[:i+1])
        
        # Calculate vals, this could be done in parallel
        feature_matrix[i][0] = this_lob.time
        feature_matrix[i][1] = this_lob.microprice()
        feature_matrix[i][2] = this_lob.total_quantity_all_quotes()
        feature_matrix[i][3] = group_lobs.average_midprice_financial_duration()
        
    tok = time.time()
    print(f'time taken for processing {tok-tik}')
    print(feature_matrix[0])

    columns=['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration']
    df = pd.DataFrame(feature_matrix,columns=columns)
    df.to_csv('test.csv')