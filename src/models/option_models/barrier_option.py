# barrier_option.py

from models.option_models.exotic_option import ExoticOption
from models.pricing_method.monte_carlo import MonteCarloPricer
from models.pricing_method.binomial_tree import BinomialTreePricer
from models.greek_method.binomial_tree_greek import BinomialTreeGreek
from models.pricing_method.black_scholes import BlackScholesPricer
from models.greek_method.black_scholes_greek import BlackScholesGreek

class BarrierOption(ExoticOption):
    def __init__(self, barrier_level, barrier_type, type_exercise: str = "European" , rebate=0, **kwargs):

        super().__init__(exotic_type='barrier', **kwargs)
        
        if barrier_type not in ['up-and-in', 'up-and-out', 'down-and-in', 'down-and-out']:
            raise ValueError("Le type de barrière doit être 'up-and-in', 'up-and-out', 'down-and-in' ou 'down-and-out'.")

        self.barrier_level = barrier_level
        self.barrier_type = barrier_type
        self.rebate = rebate
        self.type_exercise = type_exercise

    def price(self, num_paths=10000, time_steps=60):
        if self.type_exercise == "american":
            return MonteCarloPricer.price_barrier(
                type_option=self.type_option,
                spot=self.spot,
                strike=self.strike,
                maturity=self.maturity,
                rate=self.rate,
                volatility=self.volatility,
                dividend_yield=self.dividend_yield,
                barrier_level=self.barrier_level,
                barrier_type=self.barrier_type,
                rebate=self.rebate,
                num_paths=num_paths,
                time_steps=time_steps
            )
        else:
            return BlackScholesPricer.price_barrier_euro(
                type_option = self.type_option, 
                S = self.spot, 
                K = self.strike, 
                T = self.maturity, 
                r = self.rate, 
                sigma = self.volatility, 
                q = self.dividend_yield, 
                barrier = self.barrier_level, 
                barrier_type = self.barrier_type,
                rebate=self.rebate
                )
    

    def greek(self, steps=60):
        if self.type_exercise == "American":
            return BinomialTreeGreek.binomial_barrier_greeks(
                S=self.spot,
                K=self.strike,
                T=self.maturity,
                r=self.rate,
                sigma=self.volatility,
                q=self.dividend_yield,
                option_type=self.type_option,
                barrier_level=self.barrier_level,
                barrier_type=self.barrier_type,
                rebate=self.rebate,
                steps=steps
            )
    
        else:
            return BlackScholesGreek.greek_barrier_euro(
                type_option = self.type_option, 
                S = self.spot, 
                K = self.strike, 
                T = self.maturity, 
                r = self.rate, 
                sigma = self.volatility, 
                q = self.dividend_yield, 
                barrier = self.barrier_level, 
                barrier_type = self.barrier_type)



    def payoff(self):

        if self.barrier_type == "down-and-out":
            if self.spot <= self.barrier_level:
                return self.rebate  
            else:
                return max(self.spot - self.strike, 0) if self.type_option == "call" else max(self.strike - self.spot, 0)

        elif self.barrier_type == "up-and-out":
            if self.spot >= self.barrier_level:
                return self.rebate 
            else:
                return max(self.spot - self.strike, 0) if self.type_option == "call" else max(self.strike - self.spot, 0)

        elif self.barrier_type == "down-and-in":
            if self.spot > self.barrier_level:
                return self.rebate 
            else:
                return max(self.spot - self.strike, 0) if self.type_option == "call" else max(self.strike - self.spot, 0)

        elif self.barrier_type == "up-and-in":
            if self.spot < self.barrier_level:
                return self.rebate  
            else:
                return max(self.spot - self.strike, 0) if self.type_option == "call" else max(self.strike - self.spot, 0)

        else:
            raise ValueError("Type de barrière invalide.")


    
 


    def price2(self, steps=500):
        return BinomialTreePricer.price_barrier_binomial(
            type_option=self.type_option,
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            rate=self.rate,
            volatility=self.volatility,
            dividend_yield=self.dividend_yield,
            barrier_level=self.barrier_level,
            barrier_type=self.barrier_type,
            rebate=self.rebate,
            steps= steps        )