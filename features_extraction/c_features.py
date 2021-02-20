import numpy as np
import json

## Statistical features
# Takes in a number of samples and returns the AMFD

class lob:
    def __init__(self, json_lob):
        self.bid = np.array(json_lob['bid'])
        self.ask = np.array(json_lob['ask'])
        self.time = json_lob['time']

def average_midprice_financial_duration(lobs):
    prices = np.zeros(len(lobs))
    times = np.zeros(len(lobs))

    for i,lob in enumerate(lobs):
        times[i] = lob['time']
        bid = np.array(lob['bid'])
        ask = np.array(lob['ask'])
        max_bid = np.amax(bid)
        min_ask = np.amax(ask)
        prices[i] = float(min_ask-max_bid)

    mfd = np.cumsum(times)/np.cumsum(prices)
    amfd = np.mean(mfd)
    return amfd

# Microprice, volume weighted midprice
def microprice(lob):
    bid = np.array(lob['bid'])
    ask = np.array(lob['ask'])
    max_bid = np.argmax(bid)
    min_ask = np.argmin(ask)
    microprice = (bid[max_bid][0]*ask[min_ask][1] + bid[max_bid][1]*ask[min_ask][0])/(ask[min_ask][1]+bid[max_bid][1])
    return microprice

# Total quanitity of all bid ask quotes
def total_quantity_all_quotes(lob):
    bid = np.array(lob['bid'])
    ask = np.array(lob['ask'])
    total_bid = np.sum(bid[:,1])
    total_ask = np.sum(ask[:,1])
    return total_bid+total_ask


# Load sample JSON and decode into varible
with open('./feature_testing.json') as json_file:
    features = json.load(json_file)
samples = features[1:10]
sample = features[1]
print(microprice(sample))