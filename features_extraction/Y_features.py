import numpy as np

class lob:
    def __init__(self, json_lob):
        self.bid = np.array(json_lob['bid'])
        self.ask = np.array(json_lob['ask'])
        self.time = json_lob['time']

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
        self.lob_lst = [lob(lob_entry) for lob_entry in lobs]

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


def realized_quarticity():
    pass

def noise_variance():
    pass

def trading_freq():
    pass