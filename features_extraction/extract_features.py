import pandas as pd
import json
from c_features import lob, lobs

if __name__ == "__main__":
    #path = "./data/TstB02_2022-01-04tapes.csv"
    #tapes = pd.read_csv(path, header=None)
    
    with open('./feature_testing.json') as json_file:
        j_son = json.load(json_file)
    
    df = pd.DataFrame(columns=['time','microprice','total_quantity_all_quotes','average_midprice_financial_duration'])
    
    k = 10
    for i, x in enumerate(j_son):
        # Get json for this lob
        this_lob = lob(x)
        # Get groups of json given k
        if i >= k-1:
            group_lobs = lobs(j_son[(i-(k-1)):(i+1)])
        else:
            group_lobs = lobs(j_son[:i])
        
        # Calculate vals, this could be done in parallel
        new_row = {
            'time': this_lob.time,
            'microprice': this_lob.microprice(),
            'total_quantity_all_quotes': this_lob.total_quantity_all_quotes(),
            'average_midprice_financial_duration': group_lobs.average_midprice_financial_duration()
        }

        #print(new_row)
        # Append to df
        df = df.append(new_row, ignore_index=True)

    # Export as CSV
    df.to_csv('test.csv')
