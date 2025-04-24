"""Simple option pricing functions."""

import math
from typing import Dict, Union

Number = Union[int, float]


def black_scholes(stock_price: Number, 
                 strike_price: Number, 
                 time_to_expiry: Number, 
                 risk_free_rate: Number, 
                 volatility: Number, 
                 option_type: str = 'call') -> float:
    """
    Calculate option price using the Black-Scholes model.
    
    Parameters:
        stock_price: Current stock price
        strike_price: Strike price
        time_to_expiry: Time to expiration (in years)
        risk_free_rate: Risk-free interest rate (as a decimal)
        volatility: Volatility (as a decimal)
        option_type: 'call' or 'put'
        
    Returns:
        float: Option price
    """
    if time_to_expiry <= 0:
        if option_type.lower() == 'call':
            return max(0, stock_price - strike_price)
        else:
            return max(0, strike_price - stock_price)
    
    # Calculate d1 and d2
    d1 = (math.log(stock_price / strike_price) + 
          (risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    
    d2 = d1 - volatility * math.sqrt(time_to_expiry)
    
    # Calculate CDF of d1 and d2
    def norm_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    if option_type.lower() == 'call':
        price = stock_price * norm_cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm_cdf(d2)
    else:
        price = strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm_cdf(-d2) - stock_price * norm_cdf(-d1)
    
    return price


def option_delta(stock_price: Number,
                strike_price: Number,
                time_to_expiry: Number,
                risk_free_rate: Number,
                volatility: Number,
                option_type: str = 'call') -> float:
    """
    Calculate option delta (sensitivity to changes in underlying price).
    
    Parameters:
        stock_price: Current stock price
        strike_price: Strike price
        time_to_expiry: Time to expiration (in years)
        risk_free_rate: Risk-free interest rate (as a decimal)
        volatility: Volatility (as a decimal)
        option_type: 'call' or 'put'
        
    Returns:
        float: Option delta
    """
    if time_to_expiry <= 0:
        if option_type.lower() == 'call':
            return 1.0 if stock_price > strike_price else 0.0
        else:
            return -1.0 if stock_price < strike_price else 0.0
    
    # Calculate d1
    d1 = (math.log(stock_price / strike_price) + 
          (risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    
    # Calculate CDF of d1
    def norm_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    if option_type.lower() == 'call':
        return norm_cdf(d1)
    else:
        return norm_cdf(d1) - 1 