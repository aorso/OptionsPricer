# vanilla_option.py
from models.option_models.option import Option  
from models.pricing_method.black_scholes import BlackScholesPricer 
from models.pricing_method.binomial_tree import BinomialTreePricer 
from models.greek_method.black_scholes_greek import BlackScholesGreek
from models.greek_method.binomial_tree_greek import BinomialTreeGreek

class VanillaOption(Option):
    def __init__(self, type_exercise: str = "European", **kwargs):
        super().__init__(**kwargs)  
        
        if type_exercise not in ['European', 'American']:
            raise ValueError("Le type d'exercice doit être 'European' ou 'American'.")
        
        self.type_exercise = type_exercise

    def price(self, steps=100):
        if self.type_exercise == "European":
            return BlackScholesPricer.price_vanilla_euro(
                S=self.spot,
                K=self.strike,
                T=self.maturity,
                r=self.rate,
                sigma=self.volatility,
                q=self.dividend_yield,
                type_option=self.type_option)
        
        
        elif self.type_exercise == "American":
            return BinomialTreePricer.price_vanilla_american(
                S=self.spot,
                K=self.strike,
                T=self.maturity,
                r=self.rate,
                sigma=self.volatility,
                q=self.dividend_yield,
                option_type=self.type_option,
                steps=steps
            )
        else:
            raise ValueError("Type d'exercice non supporté.")
        
    def greek(self):
        if self.type_exercise == "European":
            return BlackScholesGreek.bs_greeks(
                S=self.spot,
                K=self.strike,
                T=self.maturity,
                r=self.rate,
                sigma=self.volatility,
                q=self.dividend_yield,
                option_type=self.type_option)
        
        elif self.type_exercise == "American":
            return BinomialTreeGreek.binomial_american_greeks(
                S=self.spot,
                K=self.strike,
                T=self.maturity,
                r=self.rate,
                sigma=self.volatility,
                q=self.dividend_yield,
                option_type=self.type_option,
                steps = 60)
        else:
            raise ValueError("Type d'exercice non supporté.")
            
    def payoff(self):
        if self.type_option == "call":
            return max(self.spot - self.strike, 0.0)
        elif self.type_option == "put":
            return max(self.strike - self.spot, 0.0)
        else:
            raise ValueError("type_option doit être 'call' ou 'put'.")

