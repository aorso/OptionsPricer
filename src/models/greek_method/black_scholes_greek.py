
# black_scholes_greek.py

import numpy as np
from scipy.stats import norm
from models.option_models.option import Option

class BlackScholesGreek:
    def __init__(self, option: Option):
        self.option = option

    @staticmethod
    def bs_greeks(S, K, T, r, sigma, q, option_type):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Delta
        if option_type == "call":
            delta = np.exp(-q * T) * norm.cdf(d1)
        elif option_type == "put":
            delta = np.exp(-q * T) * (norm.cdf(d1) - 1)

        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T)) * np.exp(-q * T)

        vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

        if option_type == "call":
            theta = (-S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                     - r * K * np.exp(-r * T) * norm.cdf(d2)
                     + q * S * np.exp(-q * T) * norm.cdf(d1))
        elif option_type == "put":
            theta = (-S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                     + r * K * np.exp(-r * T) * norm.cdf(-d2)
                     - q * S * np.exp(-q * T) * norm.cdf(-d1))

        if option_type == "call":
            rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == "put":
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

        return {
        "Delta": float(delta),
        "Gamma": float(gamma), 
        "Vega": float(vega),
        "Theta": float(theta),
        "Rho": float(rho),
    }


    @staticmethod
    def quanto_greek(spot, strike, maturity, rate_local, rate_foreign, vol_spot, vol_fx, rho, div_yield=0, option_type='call'):

        if option_type not in ['call', 'put']:
            raise ValueError("option_type doit être 'call' ou 'put'")
        
        # Calcul du taux ajusté
        adjusted_rate = rate_foreign - rho * vol_spot * vol_fx - div_yield


        d1 = (np.log(spot / strike) + (adjusted_rate + 0.5 * vol_spot**2) * maturity) / (vol_spot * np.sqrt(maturity))
        d2 = d1 - vol_spot * np.sqrt(maturity)


        pdf_d1 = norm.pdf(d1)
        cdf_d1 = norm.cdf(d1) if option_type == 'call' else norm.cdf(-d1)
        cdf_d2 = norm.cdf(d2) if option_type == 'call' else norm.cdf(-d2)
        
        # Facteur d'actualisation
        discount_factor = np.exp((adjusted_rate - rate_local) * maturity)
        
        # Delta
        delta = discount_factor * cdf_d1

        # Gamma
        gamma = discount_factor * pdf_d1 / (spot * vol_spot * np.sqrt(maturity))
        
        # Vega
        vega = spot * discount_factor * pdf_d1 * np.sqrt(maturity)
        
        # Theta
        theta = -(spot * discount_factor * pdf_d1 * vol_spot) / (2 * np.sqrt(maturity))
        theta -= adjusted_rate * spot * discount_factor * cdf_d1
        theta += rate_local * strike * np.exp(-rate_local * maturity) * cdf_d2
        
        # Rho
        rho_local = -strike * maturity * np.exp(-rate_local * maturity) * cdf_d2
        rho_foreign = spot * maturity * discount_factor * cdf_d1
        
        # Vega 
        vega_fx = -spot * discount_factor * cdf_d1 * rho * vol_spot * maturity
        
        # Rho
        rho_correlation = -spot * discount_factor * cdf_d1 * vol_spot * vol_fx * maturity
        
        return {
            "Delta": float(delta),
            "Gamma": float(gamma),
            "Vega": float(vega),
            "Vega (FX)": float(vega_fx),
            "Theta": float(theta),
            "Rho": float(rho_local),
            "Rho (Foreign)": float(rho_foreign),
            "Rho (Correlation)": float(rho_correlation)
        }





    def greek_barrier_euro(type_option, S, K, T, r, sigma, q, barrier, barrier_type):
 
        REPLICATION_VANILLA_Ksup = {
            "calldown-and-in": {"coef1": 0, "type_option1": "call", "coef2": 0, "type_option2": "call", "coef3": 0, "type_option3": "put"},
            "calldown-and-out": {"coef1": 1, "type_option1": "call", "coef2": 0, "type_option2": "call", "coef3": 0, "type_option3": "put"},
            "callup-and-in": {"coef1": 1, "type_option1": "call", "coef2": 0, "type_option2": "call", "coef3": 0, "type_option3": "call"},
            "callup-and-out": {"coef1": 0, "type_option1": "call", "coef2": 0, "type_option2": "call", "coef3": 0, "type_option3": "call"},
            "putdown-and-in": {"coef1": 0, "type_option1": "put", "coef2": 1, "type_option2": "put", "coef3": 1, "type_option3": "put"},
            "putdown-and-out": {"coef1": 1, "type_option1": "put", "coef2": -1, "type_option2": "put", "coef3": -1, "type_option3": "put"},
            "putup-and-in": {"coef1": 1, "type_option1": "put", "coef2": -1, "type_option2": "put", "coef3": -1, "type_option3": "put"},
            "putup-and-out": {"coef1": 0, "type_option1": "put", "coef2": 1, "type_option2": "put", "coef3": 1, "type_option3": "put"},
        }

        REPLICATION_VANILLA_Kinf = {
            "calldown-and-in": {"coef1": 1, "type_option1": "call", "coef2": -1, "type_option2": "call", "coef3": -1, "type_option3": "call"},
            "calldown-and-out": {"coef1": 0, "type_option1": "call", "coef2": 1, "type_option2": "call", "coef3": 1, "type_option3": "call"},
            "callup-and-in": {"coef1": 0, "type_option1": "call", "coef2": 1, "type_option2": "call", "coef3": 1, "type_option3": "call"},
            "callup-and-out": {"coef1": 1, "type_option1": "call", "coef2": -1, "type_option2": "call", "coef3": -1, "type_option3": "call"},
            "putdown-and-in": {"coef1": 1, "type_option1": "put", "coef2": 0, "type_option2": "put", "coef3": 0, "type_option3": "put"},
            "putdown-and-out": {"coef1": 0, "type_option1": "put", "coef2": 0, "type_option2": "put", "coef3": 0, "type_option3": "put"},
            "putup-and-in": {"coef1": 0, "type_option1": "put", "coef2": 0, "type_option2": "put", "coef3": 0, "type_option3": "put"},
            "putup-and-out": {"coef1": 1, "type_option1": "put", "coef2": 0, "type_option2": "put", "coef3": 0, "type_option3": "put"},
        }

        option_type = type_option + barrier_type

        if K>=barrier:
            config = REPLICATION_VANILLA_Ksup[option_type]

        else: 
            config = REPLICATION_VANILLA_Kinf[option_type]


        coef1, coef2, coef3 = config["coef1"], config["coef2"], config["coef3"]
        type_option1, type_option2, type_option3 = config["type_option1"], config["type_option2"], config["type_option3"]


        greeks_1 = BlackScholesGreek.bs_greeks(S, K, T, r, sigma, q, type_option1)
        greeks_2 = BlackScholesGreek.bs_greeks(S, barrier, T, r, sigma, q, type_option2)
        greeks_3 = DigitGreek.bs_greeks_digit(S, barrier, T, r, sigma, q, 1, type_option3, barrier=barrier, barrier_type=None)


        greeks_names = ["Delta", "Gamma", "Vega", "Theta", "Rho"]

        greeks_combined = {
            greek: float(
                coef1 * greeks_1.get(greek, 0) +
                coef2 * greeks_2.get(greek, 0) +
                coef3 * (K - barrier) * greeks_3.get(greek, 0)
            )
            for greek in greeks_names
        }

        return greeks_combined





class DigitGreek:
    @staticmethod
    def bs_greeks_digit(S, K, T, r, sigma, q, cash_payout, type_option, barrier=None, barrier_type=None):
        d2 = (np.log(S / K) + (r - q - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        pdf_d2 = norm.pdf(d2)
        
        # Prix de base sans barrière (ajout plus tard)
        base_price = cash_payout * np.exp(-r * T)

        # Delta
        delta = (base_price / (S * sigma * np.sqrt(T))) * pdf_d2 * np.exp(-q * T)

        # Gamma
        gamma = -(base_price / (S**2 * sigma**2 * T)) * pdf_d2 * d2 * np.exp(-q * T)

        # Vega
        vega = -base_price * pdf_d2 * d2 / sigma * np.exp(-q * T)

        # Theta
        theta = base_price * pdf_d2 * (d2 / (2 * T) + r - q) * np.exp(-q * T)

        # Rho
        rho = -cash_payout * T * np.exp(-r * T) * norm.cdf(d2) if type_option == "call" else \
            cash_payout * T * np.exp(-r * T) * norm.cdf(-d2)

        # Gestion des barrières (prix = 0 si la barrière est franchie)
        if barrier:
            if (barrier_type == "up" and S >= barrier) or (barrier_type == "down" and S <= barrier):
                delta = gamma = vega = theta = rho = 0.0

        return {
            "Delta": float(delta),
            "Gamma": float(gamma),
            "Vega": float(vega),
            "Theta": float(theta),
            "Rho": float(rho)
        }
