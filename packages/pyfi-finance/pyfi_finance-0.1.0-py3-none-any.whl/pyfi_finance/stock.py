"""Stock analysis functions."""

import numpy as np
from typing import List, Dict, Tuple, Union, Optional

Number = Union[int, float]


def calculate_returns(prices: List[Number], log_returns: bool = False) -> np.ndarray:
    """
    Calculate the returns from a price series.
    
    Parameters:
        prices: List of asset prices in chronological order
        log_returns: If True, calculate logarithmic returns, otherwise arithmetic returns
        
    Returns:
        np.ndarray: Array of returns
    """
    prices_array = np.array(prices)
    if log_returns:
        # Calculate log returns: ln(P_t / P_t-1)
        return np.log(prices_array[1:] / prices_array[:-1])
    else:
        # Calculate arithmetic returns: (P_t - P_t-1) / P_t-1
        return (prices_array[1:] / prices_array[:-1]) - 1


def moving_average(data: List[Number], window: int) -> np.ndarray:
    """
    Calculate the moving average.
    
    Parameters:
        data: List of values (prices or returns)
        window: Window size for moving average
        
    Returns:
        np.ndarray: Moving average series
    """
    data_array = np.array(data)
    weights = np.ones(window) / window
    return np.convolve(data_array, weights, mode='valid')


def exponential_moving_average(data: List[Number], span: int) -> np.ndarray:
    """
    Calculate the exponential moving average.
    
    Parameters:
        data: List of values (prices or returns)
        span: Span for EMA calculation (2 / (span + 1) is the smoothing factor)
        
    Returns:
        np.ndarray: EMA series
    """
    data_array = np.array(data)
    alpha = 2 / (span + 1)
    ema = np.zeros_like(data_array)
    ema[0] = data_array[0]
    
    for i in range(1, len(data_array)):
        ema[i] = alpha * data_array[i] + (1 - alpha) * ema[i-1]
    
    return ema


def relative_strength_index(returns: List[Number], window: int = 14) -> np.ndarray:
    """
    Calculate the Relative Strength Index (RSI).
    
    Parameters:
        returns: List of returns
        window: Window size for RSI calculation
        
    Returns:
        np.ndarray: RSI values
    """
    returns_array = np.array(returns)
    # Get gains and losses
    gains = np.maximum(returns_array, 0)
    losses = -np.minimum(returns_array, 0)
    
    # Calculate average gains and losses
    avg_gain = moving_average(gains, window)
    avg_loss = moving_average(losses, window)
    
    # Calculate RS and RSI
    rs = avg_gain / np.maximum(avg_loss, 1e-10)  # Avoid division by zero
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def bollinger_bands(prices: List[Number], window: int = 20, num_std: float = 2.0) -> Dict[str, np.ndarray]:
    """
    Calculate Bollinger Bands.
    
    Parameters:
        prices: List of asset prices
        window: Window size for moving average
        num_std: Number of standard deviations for bands
        
    Returns:
        Dict: Dictionary containing middle band, upper band, and lower band
    """
    prices_array = np.array(prices)
    
    # Calculate middle band (SMA)
    middle_band = np.zeros_like(prices_array)
    middle_band[:window-1] = np.nan
    
    # Calculate standard deviation
    std = np.zeros_like(prices_array)
    std[:window-1] = np.nan
    
    for i in range(window-1, len(prices_array)):
        window_slice = prices_array[i-window+1:i+1]
        middle_band[i] = window_slice.mean()
        std[i] = window_slice.std()
    
    # Calculate upper and lower bands
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return {
        'middle': middle_band,
        'upper': upper_band,
        'lower': lower_band
    }


def macd(prices: List[Number], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, np.ndarray]:
    """
    Calculate the Moving Average Convergence Divergence (MACD).
    
    Parameters:
        prices: List of asset prices
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal EMA period
        
    Returns:
        Dict: Dictionary containing MACD line, signal line, and histogram
    """
    prices_array = np.array(prices)
    
    # Calculate fast and slow EMAs
    fast_ema = exponential_moving_average(prices_array, fast_period)
    slow_ema = exponential_moving_average(prices_array, slow_period)
    
    # Calculate MACD line
    macd_line = fast_ema - slow_ema
    
    # Calculate signal line
    signal_line = exponential_moving_average(macd_line, signal_period)
    
    # Calculate histogram
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def beta(stock_returns: List[Number], market_returns: List[Number]) -> float:
    """
    Calculate beta (systematic risk) of a stock relative to the market.
    
    Parameters:
        stock_returns: List of stock returns
        market_returns: List of market returns (same length as stock_returns)
        
    Returns:
        float: Beta coefficient
    """
    stock_array = np.array(stock_returns)
    market_array = np.array(market_returns)
    
    # Calculate covariance and variance
    covariance = np.cov(stock_array, market_array)[0, 1]
    market_variance = np.var(market_array)
    
    return covariance / market_variance 