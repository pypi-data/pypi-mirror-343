"""Command-line interface for PyFi Finance."""

import argparse
import sys
from . import core, options, portfolio

def compound_interest_cli():
    """Command-line interface for the compound interest calculation."""
    parser = argparse.ArgumentParser(description='Calculate compound interest.')
    
    parser.add_argument('--principal', '-p', type=float, required=True,
                        help='Initial investment amount')
    parser.add_argument('--rate', '-r', type=float, required=True,
                        help='Interest rate (as a decimal, e.g., 0.05 for 5%%)')
    parser.add_argument('--time', '-t', type=float, required=True,
                        help='Time in years')
    parser.add_argument('--periods', '-n', type=int, default=1,
                        help='Number of compounding periods per year (default: 1)')
    
    args = parser.parse_args()
    
    result = core.compound_interest(
        args.principal, args.rate, args.time, args.periods
    )
    
    print(f"Principal: ${args.principal:.2f}")
    print(f"Rate: {args.rate:.2%}")
    print(f"Time: {args.time} years")
    print(f"Compounding: {args.periods} times per year")
    print(f"Final Amount: ${result:.2f}")
    
    return 0


def option_price_cli():
    """Command-line interface for the option pricing calculation."""
    parser = argparse.ArgumentParser(description='Calculate option price using Black-Scholes model.')
    
    parser.add_argument('--stock-price', '-s', type=float, required=True,
                        help='Current stock price')
    parser.add_argument('--strike-price', '-k', type=float, required=True,
                        help='Strike price')
    parser.add_argument('--time', '-t', type=float, required=True,
                        help='Time to expiration (in years)')
    parser.add_argument('--rate', '-r', type=float, required=True,
                        help='Risk-free interest rate (as a decimal, e.g., 0.05 for 5%%)')
    parser.add_argument('--volatility', '-v', type=float, required=True,
                        help='Volatility (as a decimal)')
    parser.add_argument('--type', '-y', choices=['call', 'put'], default='call',
                        help='Option type: call or put (default: call)')
    parser.add_argument('--show-delta', '-d', action='store_true',
                        help='Also display option delta')
    
    args = parser.parse_args()
    
    price = options.black_scholes(
        args.stock_price, args.strike_price, args.time, 
        args.rate, args.volatility, args.type
    )
    
    print(f"Stock Price: ${args.stock_price:.2f}")
    print(f"Strike Price: ${args.strike_price:.2f}")
    print(f"Time to Expiry: {args.time:.2f} years")
    print(f"Risk-Free Rate: {args.rate:.2%}")
    print(f"Volatility: {args.volatility:.2%}")
    print(f"Option Type: {args.type}")
    print(f"Option Price: ${price:.2f}")
    
    if args.show_delta:
        delta = options.option_delta(
            args.stock_price, args.strike_price, args.time, 
            args.rate, args.volatility, args.type
        )
        print(f"Option Delta: {delta:.4f}")
    
    return 0


def portfolio_optimize_cli():
    """Command-line interface for portfolio optimization."""
    parser = argparse.ArgumentParser(description='Optimize a portfolio using Modern Portfolio Theory.')
    
    parser.add_argument('--returns', '-r', type=float, nargs='+', required=True,
                        help='Expected returns for each asset (as decimals)')
    parser.add_argument('--cov-matrix', '-c', type=float, nargs='+', required=True,
                        help='Flattened covariance matrix (row by row)')
    parser.add_argument('--risk-free-rate', '-f', type=float, default=0.0,
                        help='Risk-free rate (as a decimal, default: 0.0)')
    parser.add_argument('--target-return', '-t', type=float,
                        help='Target portfolio return (optional)')
    
    args = parser.parse_args()
    
    # Check if the covariance matrix has the right dimensions
    n = len(args.returns)
    if len(args.cov_matrix) != n * n:
        print(f"Error: Covariance matrix should have {n*n} elements for {n} assets",
              file=sys.stderr)
        return 1
    
    # Reshape the covariance matrix
    import numpy as np
    cov_matrix = np.array(args.cov_matrix).reshape(n, n)
    
    try:
        result = portfolio.optimal_portfolio(
            args.returns, cov_matrix, args.risk_free_rate, args.target_return
        )
        
        print(f"Number of assets: {n}")
        print(f"Risk-free rate: {args.risk_free_rate:.2%}")
        
        if args.target_return:
            print(f"Target return: {args.target_return:.2%}")
            print("Minimum volatility portfolio that achieves the target return:")
        else:
            print("Maximum Sharpe ratio portfolio:")
        
        print("\nOptimal Weights:")
        for i, weight in enumerate(result['weights']):
            print(f"  Asset {i+1}: {weight:.4f}")
        
        print(f"\nExpected Return: {result['return']:.2%}")
        print(f"Volatility: {result['volatility']:.2%}")
        print(f"Sharpe Ratio: {result['sharpe_ratio']:.4f}")
        
        return 0
    
    except Exception as e:
        print(f"Error during optimization: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(compound_interest_cli()) 