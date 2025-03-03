# auto_call_option.py

from models.pricing_method.binomial_tree import BinomialTreePricer
from models.pricing_method.black_scholes import BlackScholesPricer
from models.pricing_method.monte_carlo import MonteCarloPricer
from models.greek_method.monte_carlo_greek import MonteCarloGreek

class AutoCallOption:
    def __init__(self, type_autocall, spot, rate, volatility, dividend_yield, frequency_per_year, coupon, barrier_capital, barrier_early,
                 memory_feature,barrier_coupon,  maturity=5, num_paths=7000, time_steps=200, barriers_as_percentage=True, **kwargs):
        
        self.spot = spot
        self;type_autocall = type_autocall
        self.maturity = maturity
        self.rate = rate
        self.volatility = volatility
        self.dividend_yield = dividend_yield
        self.frequency_per_year = frequency_per_year
        self.coupon = coupon
        self.barrier_capital = barrier_capital
        self.barrier_coupon = barrier_coupon
        self.barrier_early = barrier_early
        self.barriers_as_percentage = barriers_as_percentage
        self.type_autocall = "call"
        self.memory_feature = memory_feature
        self.num_paths = num_paths
        self.time_steps = time_steps




    def price(self):
        return MonteCarloPricer.price_autocall(
            spot=self.spot,
            maturity=self.maturity,
            rate=self.rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield,
            coupon=self.coupon,
            barrier_capital=self.barrier_capital,
            barrier_coupon=self.barrier_coupon,
            barrier_early=self.barrier_early,
            type_autocall=self.type_autocall,
            frequency_per_year=self.frequency_per_year,  
            memory_feature=self.memory_feature,
            barriers_as_percentage=self.barriers_as_percentage,
            num_paths= self.num_paths,
            time_steps= self.time_steps
        )




    def prob_tab(self):
        return MonteCarloGreek.proba_autocall(
            spot=self.spot,
            maturity=self.maturity,
            rate=self.rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield,
            coupon=self.coupon,
            barrier_capital=self.barrier_capital,
            barrier_coupon=self.barrier_coupon,
            barrier_early=self.barrier_early,
            type_autocall=self.type_autocall,
            frequency_per_year=self.frequency_per_year,  
            memory_feature=self.memory_feature,
            barriers_as_percentage=self.barriers_as_percentage,
            num_paths= self.num_paths,
            time_steps= self.time_steps
        )










