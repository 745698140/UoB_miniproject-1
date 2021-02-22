from typing import List, Tuple
import numpy as np

def finacial_duration(T_t2,T_t1):
    """

    Parameters
    ----------
    T_t2 : [type]
        the time instance at t2
    T_t1 : [type]
        the time instance at t2

    Returns
    -------
    [type]
        finacial duration
    """
    return T_t2-T_t1

def log_returns(price1, price2):
    """
    Parameters
    ----------
    price1 : [type]
        previous price
    price2 : [type]
        next price
    """
    return np.log(price2) - np.log(price1)

def best_ask_price(ask_limit_orders: list)->list:
    """
    Parameters
    ----------
    ask_limit_orders : list
        ask limit orders

    Returns
    -------
    list
        the best ask price and shares
    """
    sorted_alo = sorted(ask_limit_orders, key=lambda x:x[0])
    return sorted_alo[0][0]

def best_bid_price(bid_limit_orders: list)->list:
    """
    Parameters
    ----------
    bid_limit_orders : list
        bid limit orders

    Returns
    -------
    list
        the best ask price and shares
    """
    sorted_alo = sorted(bid_limit_orders, key=lambda x:x[0])
    return sorted_alo[-1][0] 

def cumulative_sum_price_levels(ask_limit_orders:list, bid_limit_orders:list,k:int)->List[float]:
    asks, _ = zip(*ask_limit_orders)
    bids, _ = zip(*bid_limit_orders)
    ask_levels = len(asks)
    bid_levels = len(bids)
    common_levels = min(ask_levels, bid_levels)
    if k > common_levels:
        # print(f"{k} is out of bounds, we replace it with {common_levels}")
        k = common_levels
    return [sum(asks[:common_levels]), sum(bids[:common_levels])]

##Volatility
def realized_kernel():
    pass

def average_midprice_financial_duration(times, prices):
    mfd = np.cumsum(times)/np.cumsum(prices)
    amfd = np.mean(mfd)
    return amfd

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
    
    

def spot_volatility():
    pass

#Noise and uncertainty
def realized_quarticity_tripower():
    pass

# Price discovery features
def mid_price_weighted_by_order_imbalance(ask_limit_orders:list, bid_limit_orders:list):
    bap = best_ask_price(ask_limit_orders)
    blo = best_bid_price(bid_limit_orders)
    return (bap[0]*bap[1]+blo[0]*blo[1])/(bap[1]+blo[1])
    
def normalized_bid_ask_spread(spread:float,tick_size:float):
    return spread/tick_size
    
