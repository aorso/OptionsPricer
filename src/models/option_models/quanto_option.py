
# quanto_option.py

from models.option_models.option import Option
from models.pricing_method.black_scholes import BlackScholesPricer
from models.greek_method.black_scholes_greek import BlackScholesGreek

class QuantoOption(Option):
    def __init__(self, spot, strike, maturity, rate_local, rate_foreign, vol_fx, fx_correlation, option_type="call", **kwargs):
        super().__init__(spot=spot, strike=strike, maturity=maturity, rate=rate_local, **kwargs)
        self.rate_local = rate_local
        self.rate_foreign = rate_foreign
        self.vol_spot = self.volatility
        self.vol_fx = vol_fx
        self.fx_correlation = fx_correlation
        self.option_type = option_type

    def price(self):
        return BlackScholesPricer.quanto_price(
            spot=self.spot, 
            strike=self.strike, 
            maturity=self.maturity, 
            rate_local=self.rate_local, 
            rate_foreign=self.rate_foreign, 
            vol_spot=self.vol_spot, 
            vol_fx=self.vol_fx, 
            rho=self.fx_correlation, 
            option_type=self.option_type
        )

    def greek(self):
        return BlackScholesGreek.quanto_greek(
            spot=self.spot, 
            strike=self.strike, 
            maturity=self.maturity, 
            rate_local=self.rate_local, 
            rate_foreign=self.rate_foreign, 
            vol_spot=self.vol_spot, 
            vol_fx=self.vol_fx, 
            rho=self.fx_correlation, 
            option_type=self.option_type)
    
    def payoff(self):
        return max(0, self.spot - self.strike) if self.option_type == "call" else max(0, self.strike - self.spot)