"""Core financial calculation functions."""

import math
from typing import Union, List, Dict, Tuple, Optional

Number = Union[int, float]


def compound_interest(principal: Number, 
                      rate: Number, 
                      time: Number, 
                      periods_per_year: int = 1) -> float:
    """
    Calculate compound interest.
    
    Parameters:
        principal: Initial investment amount
        rate: Interest rate (as a decimal, e.g., 0.05 for 5%)
        time: Time in years
        periods_per_year: Number of compounding periods per year
        
    Returns:
        float: Final amount after compound interest
    """
    rate_per_period = rate / periods_per_year
    num_periods = time * periods_per_year
    return principal * (1 + rate_per_period) ** num_periods


def present_value(future_value: Number, 
                  rate: Number, 
                  time: Number, 
                  periods_per_year: int = 1) -> float:
    """
    Calculate the present value of a future amount.
    
    Parameters:
        future_value: Future amount
        rate: Discount rate (as a decimal, e.g., 0.05 for 5%)
        time: Time in years
        periods_per_year: Number of discounting periods per year
        
    Returns:
        float: Present value of the future amount
    """
    rate_per_period = rate / periods_per_year
    num_periods = time * periods_per_year
    return future_value / (1 + rate_per_period) ** num_periods


def npv(cash_flows: List[Number], 
        rate: Number, 
        initial_investment: Number = 0) -> float:
    """
    Calculate Net Present Value (NPV) of a series of cash flows.
    
    Parameters:
        cash_flows: List of cash flows
        rate: Discount rate (as a decimal, e.g., 0.05 for 5%)
        initial_investment: Initial investment (negative cash flow at time 0)
        
    Returns:
        float: Net Present Value
    """
    total = -initial_investment
    for i, cf in enumerate(cash_flows, start=1):
        total += cf / (1 + rate) ** i
    return total


def irr(cash_flows: List[Number], 
        guess: float = 0.1, 
        tolerance: float = 1e-6, 
        max_iterations: int = 100) -> Optional[float]:
    """
    Calculate Internal Rate of Return (IRR) using Newton-Raphson method.
    
    Parameters:
        cash_flows: List of cash flows (first value is the initial investment as negative)
        guess: Initial guess for the IRR
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations
        
    Returns:
        float or None: IRR if convergence is reached, None otherwise
    """
    r = guess
    
    for _ in range(max_iterations):
        npv = cash_flows[0]
        dnpv = 0
        
        for i, cf in enumerate(cash_flows[1:], start=1):
            npv += cf / (1 + r) ** i
            dnpv -= i * cf / (1 + r) ** (i + 1)
        
        if abs(npv) < tolerance:
            return r
        
        if dnpv == 0:
            return None
        
        r_new = r - npv / dnpv
        if abs(r_new - r) < tolerance:
            return r_new
        
        r = r_new
    
    return None  # Failed to converge


def monthly_payment(principal: Number, 
                    annual_rate: Number, 
                    years: Number) -> float:
    """
    Calculate monthly payment for a loan.
    
    Parameters:
        principal: Loan amount
        annual_rate: Annual interest rate (as a decimal, e.g., 0.05 for 5%)
        years: Loan term in years
        
    Returns:
        float: Monthly payment amount
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return principal / num_payments
    
    return principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
           ((1 + monthly_rate) ** num_payments - 1)


def amortization_schedule(principal: Number, 
                          annual_rate: Number, 
                          years: Number) -> List[Dict[str, float]]:
    """
    Generate an amortization schedule for a loan.
    
    Parameters:
        principal: Loan amount
        annual_rate: Annual interest rate (as a decimal, e.g., 0.05 for 5%)
        years: Loan term in years
        
    Returns:
        List[Dict]: List of dictionaries containing payment details for each period
    """
    monthly_rate = annual_rate / 12
    num_payments = int(years * 12)
    payment = monthly_payment(principal, annual_rate, years)
    
    remaining = principal
    schedule = []
    
    for period in range(1, num_payments + 1):
        interest_payment = remaining * monthly_rate
        principal_payment = payment - interest_payment
        remaining -= principal_payment
        
        schedule.append({
            'period': period,
            'payment': payment,
            'principal': principal_payment,
            'interest': interest_payment,
            'remaining': max(0, remaining)  # Adjust for floating point errors
        })
    
    return schedule 