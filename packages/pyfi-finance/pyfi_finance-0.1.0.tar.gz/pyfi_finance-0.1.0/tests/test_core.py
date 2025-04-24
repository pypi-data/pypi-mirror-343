import unittest
from pyfi_finance.core import compound_interest, present_value, npv, monthly_payment

class TestCoreFunctions(unittest.TestCase):
    
    def test_compound_interest(self):
        # Test simple case with annual compounding
        self.assertAlmostEqual(
            compound_interest(1000, 0.05, 5, 1),
            1276.28, 
            places=2
        )
        
        # Test with quarterly compounding
        self.assertAlmostEqual(
            compound_interest(1000, 0.05, 5, 4),
            1282.85, 
            places=2
        )
    
    def test_present_value(self):
        # Test simple case with annual discounting
        self.assertAlmostEqual(
            present_value(1000, 0.05, 5, 1),
            783.53, 
            places=2
        )
    
    def test_npv(self):
        # Test NPV calculation
        cash_flows = [100, 200, 300, 400]
        initial_investment = 800
        self.assertAlmostEqual(
            npv(cash_flows, 0.1, initial_investment),
            83.93, 
            places=2
        )
    
    def test_monthly_payment(self):
        # Test mortgage payment calculation
        self.assertAlmostEqual(
            monthly_payment(100000, 0.05, 30),
            536.82, 
            places=2
        )
        
        # Test with zero interest
        self.assertAlmostEqual(
            monthly_payment(100000, 0, 10),
            833.33, 
            places=2
        )

if __name__ == '__main__':
    unittest.main() 