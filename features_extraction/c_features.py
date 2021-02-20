import numpy as np
import json

class lob:
    def __init__(self, json_lob):
        self.bid = np.array(json_lob['bid'])
        self.ask = np.array(json_lob['ask'])
        self.time = json_lob['time']

    # Microprice, volume weighted midprice
    def microprice(self):
        max_bid = np.argmax(self.bid)
        min_ask = np.argmin(self.ask)
        microprice = (self.bid[max_bid][0]*self.ask[min_ask][1] + self.bid[max_bid][1]*self.ask[min_ask][0])/(self.ask[min_ask][1]+self.bid[max_bid][1])
        return microprice

    # Total quanitity of all bid ask quotes
    def total_quantity_all_quotes(self):
        total_bid = np.sum(self.bid[:,1])
        total_ask = np.sum(self.ask[:,1])
        return total_bid+total_ask

class lobs:
    def __init__(self, lobs):
        self.lob_lst = [lob(lob_entry) for lob_entry in lobs]

    # Take in a list of lobs and calculate AMFD
    def average_midprice_financial_duration(self):
        prices = np.zeros(len(self.lob_lst))
        times = np.zeros(len(self.lob_lst))
        
        for i,lob in enumerate(self.lob_lst):
            times[i] = lob.time
            max_bid = np.amax(lob.bid)
            min_ask = np.amax(lob.ask)
            prices[i] = float(min_ask-max_bid)

        mfd = np.cumsum(times)/np.cumsum(prices)
        amfd = np.mean(mfd)
        return amfd

if __name__ == '__main__':
    # Load sample JSON and decode into varible
    with open('./feature_testing.json') as json_file:
        features = json.load(json_file)
    samples = features[1:10]
    sample = features[1]

    lob_sample = lob(sample)
    print(lob_sample.microprice())

    lob_samples = lobs(samples)
    print(lob_samples.average_midprice_financial_duration())