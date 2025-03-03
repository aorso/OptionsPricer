# strategy_analysis.py


from models.option_models.vanilla_option import VanillaOption
# strategy_analysis.py

from models.option_models.vanilla_option import VanillaOption


class OptionStrategy:
    def __init__(
        self,
        strategy_type,
        spot,
        rate,
        maturity=1.0,
        time_type="years",
        dividend_yield=0.0,
        type_exercise="European",
        # On prévoit jusqu'à 4 options max
        strike_1=None,
        volatility_1=None,
        strike_2=None,
        volatility_2=None,
        strike_3=None,
        volatility_3=None,
        strike_4=None,
        volatility_4=None):
        
        self.strategy_type = strategy_type.lower()
        self.spot = spot
        self.rate = rate
        self.maturity = maturity
        self.time_type = time_type
        self.dividend_yield = dividend_yield
        self.type_exercise = type_exercise

        self.strike_1 = strike_1
        self.volatility_1 = volatility_1
        self.strike_2 = strike_2
        self.volatility_2 = volatility_2
        self.strike_3 = strike_3
        self.volatility_3 = volatility_3
        self.strike_4 = strike_4
        self.volatility_4 = volatility_4

        self.options_params = []
        self.coefficients = []
        self._create_options_params()

        self.options = [VanillaOption(**params) for params in self.options_params]

    def _create_options_params(self):

        strategy_info = {
            "call_spread": {
                "n_options": 2,
                "types": ["call", "call"],   # 1er call long, 2e call short
                "coeffs": [1, -1]
            },
            "put_spread": {
                "n_options": 2,
                "types": ["put", "put"],     # 1er put short, 2e put long (ou inverse selon convention)
                "coeffs": [-1, 1]
            },
            "straddle": {
                "n_options": 2,
                "types": ["call", "put"],     # call + put
                "coeffs": [1, 1]
            },
            "strangle": {
                "n_options": 2,
                "types": ["call", "put"],  # call + put OTM
                "coeffs": [1, 1]
            },
            "butterfly": {
                "n_options": 3,
                "types": ["call", "call", "call"],  # long call (K1), short 2 calls (K2), long call (K3)
                "coeffs": [1, -2, 1]
            },
            "condor": {
                "n_options": 4,
                "types": ["call", "call", "call", "call"],  # long K1, short K2, short K3, long K4
                "coeffs": [1, -1, -1, 1]
            },
            "risk_reversal": {
                "n_options": 2,
                "types": ["call", "put"],  # long call + short put, par ex.
                "coeffs": [1, -1]
            },
        }


        if self.strategy_type not in strategy_info:
            raise ValueError(f"Stratégie non supportée : {self.strategy_type}")


        cfg = strategy_info[self.strategy_type]
        n_options = cfg["n_options"]
        option_types = cfg["types"]  
        self.coefficients = cfg["coeffs"] 


        strikes = [
            self.strike_1,
            self.strike_2,
            self.strike_3,
            self.strike_4
        ][:n_options]

        volatilities = [
            self.volatility_1,
            self.volatility_2,
            self.volatility_3,
            self.volatility_4
        ][:n_options]


        for i in range(n_options):
            if strikes[i] is None or volatilities[i] is None:
                raise ValueError(
                    f"Paramètres manquants pour l'option #{i+1}. "
                    f"Strike et volatility sont nécessaires pour la stratégie '{self.strategy_type}'."
                )


        self.options_params = []
        for i in range(n_options):
            param_dict = {
                "type_option": option_types[i], 
                "spot": self.spot,
                "strike": strikes[i],
                "rate": self.rate,
                "volatility": volatilities[i],
                "dividend_yield": self.dividend_yield,
                "maturity": self.maturity,
                "time_type": self.time_type,
                "type_exercise": self.type_exercise,
            }
            self.options_params.append(param_dict)

    def price(self):
        return sum(
            coef * VanillaOption.price(option) 
            for option, coef in zip(self.options, self.coefficients)
        )

    def greek(self):
        total_greeks = {"Delta": 0, "Gamma": 0, "Vega": 0, "Theta": 0, "Rho": 0}

        for option, coef in zip(self.options, self.coefficients):
            option_greeks = VanillaOption.greek(option)
            for key in total_greeks:
                total_greeks[key] += coef * option_greeks.get(key, 0)

        return total_greeks

    def payoff(self):
        return sum(
            coef * VanillaOption.payoff(option)
            for option, coef in zip(self.options, self.coefficients)
        )
