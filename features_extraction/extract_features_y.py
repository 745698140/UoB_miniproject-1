from Y_features import lob, lobs
import json
import pandas as pd
import time
import numpy as np

if __name__ == "__main__":
    with open('./feature_testing.json') as json_file:
        j_son = json.load(json_file)

    df = pd.DataFrame(columns=['time', 'best_ask_price', 'best_bid_price', 'mid_price', 'mid_price_deeper_levels',
                               'realized_variance', 'positive_RV', 'negative_RV', 'jump_variation'])

    k = 10

    for i, x in enumerate(j_son):
        this_lob = lob(x)

        if i >= k-1:
            group_lobs = lobs(j_son[(i-(k-1)) : (i+1)])
        else:
            group_lobs = lobs(j_son[:i+1])

        new_row = {
            'time': this_lob.time,
            'best_ask_price': this_lob.best_ask_price(),
            'best_bid_price': this_lob.best_bid_price(),
            'mid_price': this_lob.mid_price(),
            'mid_price_deeper_levels': this_lob.mid_price_deeper_levels(),
            'realized_variance': group_lobs.realized_variance(),
            'positive_RV': group_lobs.positive_realized_semi_variance(),
            'negative_RV': group_lobs.negative_realized_semi_variance(),
            'jump_variation': group_lobs.jump_variation()
        }

        df = df.append(new_row, ignore_index = True)

    df.to_csv('test.csv')