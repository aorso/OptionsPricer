
# digits_options.py

import numpy as np
from scipy.stats import norm
from models.option_models.option import Option  
from models.greek_method.black_scholes_greek import DigitGreek
from models.pricing_method.black_scholes import BlackScholesPricer


class DigitOption(Option):
    def __init__(self, type_option, cash_payout, barrier=None, barrier_type=None,   **kwargs):

        super().__init__(type_option=type_option, **kwargs)  
        self.cash_payout = cash_payout
        self.barrier = barrier
        self.barrier_type = barrier_type.lower() if barrier_type else None

        # Validation du type de barrière
        if self.barrier_type not in (None, 'up', 'down'):
            raise ValueError("barrier_type doit être 'up', 'down' ou None.")



    def price(self):
        return BlackScholesPricer.price_option_digital(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            rate=self.rate,
            volatility=self.volatility,
            cash_payout=self.cash_payout,
            type_option=self.type_option,
            barrier=self.barrier,
            barrier_type=self.barrier_type,
            dividend_yield=self.dividend_yield,
        )



    def greek(self):
        return DigitGreek.bs_greeks_digit(
        S=self.spot,
        K=self.strike,
        T=self.maturity,
        r=self.rate,
        sigma=self.volatility,
        q=self.dividend_yield,
        cash_payout=self.cash_payout,
        type_option= self.type_option,
        barrier=self.barrier,
        barrier_type=self.barrier_type
    )


    def payoff(self):
        if self.type_option == "call":
            return self.cash_payout if self.spot >= self.strike else 0.0
        elif self.type_option == "put":
            return self.cash_payout if self.spot <= self.strike else 0.0
        else:
            raise ValueError("type_option doit être 'call' ou 'put'.")
