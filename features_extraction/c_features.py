import numpy as np
import json # Only need this to turn json obj into dict for testing

class lob:
    def __init__(self, json_lob):
        self.bid = np.array(json_lob['bid'])
        self.ask = np.array(json_lob['ask'])
        self.time = float(json_lob['time'])
        # In the form [p,n]
        self.max_bid = self.bid[np.argmax(self.bid[:,0])]
        self.min_ask = self.ask[np.argmin(self.ask[:,0])]

    # Microprice, volume weighted midprice
    def microprice(self):
        microprice = (self.max_bid[0]*self.min_ask[1] + self.max_bid[1]*self.min_ask[0])/ \
        (self.min_ask[1]+self.max_bid[1])
        return microprice

    # Total quanitity of all bid ask quotes
    def total_quantity_all_quotes(self):
        total_bid = np.sum(self.bid[:,1])
        total_ask = np.sum(self.ask[:,1])
        return total_bid+total_ask
    
    def volume_imbalance(self):
        v_bid = np.sum(self.bid[:,1])
        v_ask = np.sum(self.ask[:,1])
        vol_imbalance = v_bid/(v_ask+v_bid)
        return vol_imbalance

    def cumulative_sum_price_levels(self, k:int):
        common_levels = min(len(self.ask), len(self.bid))
        if k > common_levels:
            # print(f"{k} is out of bounds, we replace it with {common_levels}")
            k = common_levels
        return [sum(self.bid[:k, 1]), sum(self.ask[:k, 1])]
    
    def mid_price_weighted_by_order_imbalance(self):
        return sum(self.bid[:,0]*self.bid[:1] + self.ask[:,0]*self.ask[:1])/(self.bid[:,1] + self.ask[:,1])

    # price discovery features
    def normalized_bid_ask_spread(spread:float,tick_size:float):
        return spread/tick_size

    # volatility
    def realized_bipower_variation(return1:list, return2:list) -> float:
        """
        Parameters
        ----------
        return1 : list
            r(X)_i
        return2 : list
            r(X)_{i-1} or r(X)_{i-2}

        Returns
        -------
        float
        """
        return np.pi/2*(abs(return1)*abs(return2).sum())

    def best_ask_price(self):
        sorted_ask_list = sorted(self.ask, key=lambda x: x[0])
        return sorted_ask_list[0][0]

    def best_bid_price(self):
        sorted_bid_list = sorted(self.bid, key=lambda x: x[0])
        return sorted_bid_list[-1][0]

    def mid_price(self):
        return (self.best_bid_price() + self.best_ask_price()) / 2

    # define the depth of LOB as 2 initially
    def mid_price_deeper_levels(self, depth = 2):
        sorted_ask_list = sorted(self.ask, key=lambda x: x[0])
        sorted_bid_list = sorted(self.bid, key=lambda x: x[0])
        return (sorted_ask_list[depth-1][0] + sorted_bid_list[-(depth-1)][0]) / 2

    def competitive_equilibrium_price(self):
        # need the transaction data, fix it later
        pass

    def bid_ask_spread(self):
        return (self.best_bid_price() - self.best_ask_price())


class lobs:
    def __init__(self, lobs):
        self.lob_lst = lobs

    # Take in a list of lobs and calculate AMFD
    def average_midprice_financial_duration(self):
        prices = np.zeros(len(self.lob_lst))
        times = np.zeros(len(self.lob_lst))
        
        for i,lob in enumerate(self.lob_lst):
            times[i] = lob.time
            prices[i] = float(lob.min_ask[0]-lob.max_bid[0])

        mfd = np.cumsum(times)/np.cumsum(prices)
        amfd = np.mean(mfd)
        return amfd
    
    def average_spot_volatility(self):
        sv = 0
        dt = 0
        for lob in self.lob_lst:
            # Coming from lob spot volatility
            sv += lob.spot_volatility()
            dt += lob.time
        return sv / dt
    # This is just realized var
    def quadratic_int_var(self):
        pass

    def realized_pre_avg_var(self):
        pass

    def realized_bipower_semivar(self):
        pass

    #get this from the tapes rather than 
    def trading_volume(self):
        pass

    def realized_variance(self):
        # https://www.wallstreetmojo.com/realized-volatility/
        # a little problem about the RV, cause it need the return to calculate
        lst_len = len(self.lob_lst)
        if lst_len < 2:
            return 0
        else:
            RV_sum = 0
            for i in range(lst_len - 1):
                r1 = self.lob_lst[i].mid_price()
                r2 = self.lob_lst[i+1].mid_price()
                RV_sum += np.square(np.log(r2) - np.log(r1))
            return RV_sum

    def positive_realized_semi_variance(self):
        lst_len = len(self.lob_lst)
        if lst_len < 2:
            return 0
        else:
            positive_RV_sum = 0
            for i in range(lst_len - 1):
                r1 = self.lob_lst[i].mid_price()
                r2 = self.lob_lst[i+1].mid_price()
                if r2 >= r1:
                    positive_RV_sum += np.square(np.log(r2) - np.log(r1))
            return positive_RV_sum

    def negative_realized_semi_variance(self):
        lst_len = len(self.lob_lst)
        if lst_len < 2:
            return 0
        else:
            negative_RV_sum = 0
            for i in range(lst_len - 1):
                r1 = self.lob_lst[i].mid_price()
                r2 = self.lob_lst[i + 1].mid_price()
                if r2 <= r1:
                    negative_RV_sum += np.square(np.log(r2) - np.log(r1))
            return negative_RV_sum

    def realized_bipower_variation(self):
        lst_len = len(self.lob_lst)
        if lst_len < 3:
            return 0
        else:
            BV_sum = 0
            for i in range(lst_len - 2):
                r1 = self.lob_lst[i].mid_price()
                r2 = self.lob_lst[i+1].mid_price()
                r3 = self.lob_lst[i+2].mid_price()
                BV_sum += (np.pi / 2) * (abs(np.log(r2)-np.log(r1))) * (abs(np.log(r3) - np.log(r2)))
            return BV_sum

    def jump_variation(self):
        lst_len = len(self.lob_lst)
        RV = self.realized_variance()
        BV = self.realized_bipower_variation()
        return max(RV-BV, 0)




if __name__ == '__main__':
    # Load sample JSON and decode into varible
    with open('./feature_testing.json') as json_file:
        features = json.load(json_file)
    
    samples = features[1:10]
    sample = features[10]

    lob_sample = lob(sample)
    print(lob_sample.volume_imbalance())

    lob_samples = lobs(samples)
    print(lob_samples.average_midprice_financial_duration())