"""Portfolio analysis and optimization functions."""

import numpy as np
from typing import List, Dict, Tuple, Union, Optional

Number = Union[int, float]


def portfolio_return(returns: List[Number], weights: List[Number]) -> float:
    """
    Calculate the expected return of a portfolio.
    
    Parameters:
        returns: List of expected returns for each asset
        weights: List of weights for each asset (must sum to 1)
        
    Returns:
        float: Expected portfolio return
    """
    return sum(r * w for r, w in zip(returns, weights))


def portfolio_volatility(returns: List[Number], 
                         weights: List[Number], 
                         cov_matrix: np.ndarray) -> float:
    """
    Calculate the volatility (standard deviation) of a portfolio.
    
    Parameters:
        returns: List of expected returns for each asset
        weights: List of weights for each asset (must sum to 1)
        cov_matrix: Covariance matrix of asset returns
        
    Returns:
        float: Portfolio volatility
    """
    weights_array = np.array(weights)
    return np.sqrt(weights_array.T @ cov_matrix @ weights_array)


def sharpe_ratio(portfolio_return: float, 
                 portfolio_volatility: float, 
                 risk_free_rate: float = 0.0) -> float:
    """
    Calculate the Sharpe ratio for a portfolio.
    
    Parameters:
        portfolio_return: Expected portfolio return
        portfolio_volatility: Portfolio volatility (standard deviation)
        risk_free_rate: Risk-free rate of return
        
    Returns:
        float: Sharpe ratio
    """
    return (portfolio_return - risk_free_rate) / portfolio_volatility


def optimal_portfolio(returns: List[Number], 
                      cov_matrix: np.ndarray, 
                      risk_free_rate: float = 0.0,
                      target_return: Optional[float] = None) -> Dict:
    """
    Find the optimal portfolio weights using Modern Portfolio Theory.
    
    If target_return is None, finds the maximum Sharpe ratio portfolio.
    If target_return is specified, finds the minimum volatility portfolio
    that achieves the target return.
    
    Parameters:
        returns: List of expected returns for each asset
        cov_matrix: Covariance matrix of asset returns
        risk_free_rate: Risk-free rate of return
        target_return: Target portfolio return (optional)
        
    Returns:
        dict: Dictionary containing optimal weights and portfolio metrics
    """
    import scipy.optimize as sco
    
    num_assets = len(returns)
    
    def portfolio_volatility_func(weights):
        return portfolio_volatility(returns, weights, cov_matrix)
    
    def portfolio_return_func(weights):
        return portfolio_return(returns, weights)
    
    # Constraints and bounds
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # weights sum to 1
    bounds = tuple((0, 1) for _ in range(num_assets))  # weights between 0 and 1
    
    # Initial guess: equal weights
    initial_weights = np.ones(num_assets) / num_assets
    
    if target_return is None:
        # Maximize Sharpe ratio
        def neg_sharpe_ratio(weights):
            p_ret = portfolio_return_func(weights)
            p_vol = portfolio_volatility_func(weights)
            return -(p_ret - risk_free_rate) / p_vol
        
        result = sco.minimize(neg_sharpe_ratio, initial_weights, 
                              method='SLSQP', bounds=bounds, 
                              constraints=constraints)
        optimal_weights = result['x']
    else:
        # Minimize volatility subject to target return
        constraints.append({
            'type': 'eq', 
            'fun': lambda x: portfolio_return_func(x) - target_return
        })
        
        result = sco.minimize(portfolio_volatility_func, initial_weights, 
                             method='SLSQP', bounds=bounds, 
                             constraints=constraints)
        optimal_weights = result['x']
    
    # Calculate portfolio metrics
    opt_return = portfolio_return_func(optimal_weights)
    opt_volatility = portfolio_volatility_func(optimal_weights)
    opt_sharpe = sharpe_ratio(opt_return, opt_volatility, risk_free_rate)
    
    return {
        'weights': optimal_weights,
        'return': opt_return,
        'volatility': opt_volatility,
        'sharpe_ratio': opt_sharpe
    }


def efficient_frontier(returns: List[Number], 
                       cov_matrix: np.ndarray, 
                       risk_free_rate: float = 0.0,
                       points: int = 20) -> List[Dict]:
    """
    Generate points along the efficient frontier.
    
    Parameters:
        returns: List of expected returns for each asset
        cov_matrix: Covariance matrix of asset returns
        risk_free_rate: Risk-free rate of return
        points: Number of points to generate
        
    Returns:
        List[Dict]: List of dictionaries containing portfolio metrics for each point
    """
    # Find the range of returns to evaluate
    min_vol_port = optimal_portfolio(returns, cov_matrix, risk_free_rate)
    
    # Use a range from slightly below min return to slightly above max return
    target_returns = np.linspace(min(returns) * 0.8, max(returns) * 1.2, points)
    efficient_ports = []
    
    for target in target_returns:
        try:
            port = optimal_portfolio(returns, cov_matrix, risk_free_rate, target)
            efficient_ports.append(port)
        except:
            # Skip points that can't be optimized (might be outside feasible range)
            continue
    
    return efficient_ports 