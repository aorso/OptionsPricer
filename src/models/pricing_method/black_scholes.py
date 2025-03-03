
# black_scholes.py
import math
from math import log, sqrt, exp
import numpy as np
import pandas as pd
from scipy.stats import norm
from models.option_models.option import Option

class BlackScholesPricer:
    def __init__(self, option: Option):
        self.option = option

    def price_vanilla_euro(S, K, T, r, sigma, q, type_option):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if type_option == "call":
            price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif type_option == "put":
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        return price
    

    def price_option_digital(spot, strike, maturity, rate, volatility, cash_payout, type_option, barrier=None, barrier_type=None, dividend_yield=0.0):

     
        d2 = (np.log(spot / strike) + (rate - dividend_yield - 0.5 * volatility**2) * maturity) / (volatility * np.sqrt(maturity))

        base_price = cash_payout * np.exp(-rate * maturity)

        if type_option == "call":
            price = base_price * norm.cdf(d2)
        elif type_option == "put":
            price = base_price * (1 - norm.cdf(d2))
        else:
            raise ValueError("type_option doit être 'call' ou 'put'.")


        return price


    def price_barrier_euro(type_option, S, K, T, r, sigma, q, barrier, barrier_type, rebate=0):
        
        REPLICATION_VANILLA_Ksup = {
            "calldown-and-in":  {"coef1": 0, "type_option1" : "call", "coef2" : 0, "type_option2": "call","coef3" : 0 , "type_option3": "put"},
            "calldown-and-out":  {"coef1": 1, "type_option1" : "call", "coef2" : 0, "type_option2": "call","coef3" : 0 , "type_option3": "put"},
            "callup-and-in":   {"coef1": 1, "type_option1" : "call", "coef2" : 0, "type_option2": "call","coef3" : 0 , "type_option3": "call"},
            "callup-and-out":  {"coef1": 0, "type_option1" : "call", "coef2" : 0, "type_option2": "call","coef3" : 0 , "type_option3": "call"},
            
            "putdown-and-in":  {"coef1": 0, "type_option1" : "put", "coef2" : 1, "type_option2": "put","coef3" : 1 , "type_option3": "put"},
            "putdown-and-out":  {"coef1": 1, "type_option1" : "put", "coef2" : -1, "type_option2": "put","coef3" : -1 , "type_option3": "put"},
            "putup-and-in":   {"coef1": 1, "type_option1" : "put", "coef2" : -1, "type_option2": "put","coef3" : -1 , "type_option3": "put"},
            "putup-and-out":  {"coef1": 0, "type_option1" : "put", "coef2" : 1, "type_option2": "put","coef3" : 1 , "type_option3": "put"},
        }

        REPLICATION_VANILLA_Kinf = {
            "calldown-and-in":  {"coef1": 1, "type_option1" : "call", "coef2" : -1, "type_option2": "call","coef3" : -1 , "type_option3": "call"},
            "calldown-and-out":  {"coef1": 0, "type_option1" : "call", "coef2" : 1, "type_option2": "call","coef3" : 1 , "type_option3": "call"},
            "callup-and-in":   {"coef1": 0, "type_option1" : "call", "coef2" : 1, "type_option2": "call","coef3" : 1 , "type_option3": "call"},
            "callup-and-out":  {"coef1": 1, "type_option1" : "call", "coef2" : -1, "type_option2": "call","coef3" : -1 , "type_option3": "call"},
            
            "putdown-and-in":  {"coef1": 1, "type_option1" : "put", "coef2" : 0, "type_option2": "put","coef3" : 0 , "type_option3": "put"},
            "putdown-and-out":  {"coef1": 0, "type_option1" : "put", "coef2" : 0, "type_option2": "put","coef3" : 0 , "type_option3": "put"},
            "putup-and-in":   {"coef1": 0, "type_option1" : "put", "coef2" : 0, "type_option2": "put","coef3" : 0 , "type_option3": "put"},
            "putup-and-out":  {"coef1": 1, "type_option1" : "put", "coef2" : 0, "type_option2": "put","coef3" : 0 , "type_option3": "put"},
        }


        option_type = type_option + barrier_type

        if K >= barrier:
            config = REPLICATION_VANILLA_Ksup[option_type]
        else: 
            config = REPLICATION_VANILLA_Kinf[option_type]

        type_option1 = config["type_option1"]
        type_option2 = config["type_option2"]
        type_option3 = config["type_option3"]

        coef1 = config["coef1"]
        coef2 = config["coef2"]
        coef3 = config["coef3"]

        prix= (coef1* BlackScholesPricer.price_vanilla_euro(S, K, T, r, sigma, q, type_option1) 
                + coef2 * BlackScholesPricer.price_vanilla_euro(S, barrier, T, r, sigma, q, type_option2) 
                + coef3 * (K-barrier) * BlackScholesPricer.price_option_digital(S, barrier, T, r, sigma, 1, type_option3, barrier=barrier, barrier_type=None, dividend_yield=q))
        
        if rebate != 0:
            barrier_type_lower = barrier_type.lower()

            if  barrier_type_lower in ["down-and-in", "up-and-out"]:
                rebate_price =  BlackScholesPricer.price_option_digital(S, barrier, T, r, sigma, rebate, type_option="put",barrier=barrier, barrier_type=None, dividend_yield=q)

            elif barrier_type_lower in ["down-and-out", "up-and-in"]:

                rebate_price =  BlackScholesPricer.price_option_digital(S, barrier, T, r, sigma, rebate, type_option="call",barrier=barrier, barrier_type=None, dividend_yield=q)

            prix += rebate_price

        return prix


    def quanto_price(spot, strike, maturity, rate_local, rate_foreign, vol_spot, vol_fx, rho, option_type='call'):
    
        # Validation des paramètres
        if not -1 <= rho <= 1:
            raise ValueError("La corrélation doit être comprise entre -1 et 1")
        
        if maturity <= 0:
            raise ValueError("La maturité doit être positive")
            
        if vol_spot <= 0 or vol_fx <= 0:
            raise ValueError("Les volatilités doivent être positives")
            
        if spot <= 0 or strike <= 0:
            raise ValueError("Le spot et le strike doivent être positifs")
        
        if option_type not in ['call', 'put']:
            raise ValueError("option_type doit être 'call' ou 'put'")

        adjusted_rate = rate_foreign - rho * vol_spot * vol_fx
        
        d1 = (np.log(spot / strike) + (adjusted_rate + 0.5 * vol_spot**2) * maturity) / (vol_spot * np.sqrt(maturity))
        d2 = d1 - vol_spot * np.sqrt(maturity)
        
        if option_type == 'call':
            price = (spot * np.exp((adjusted_rate - rate_local) * maturity) * norm.cdf(d1) -
                    strike * np.exp(-rate_local * maturity) * norm.cdf(d2))
        else:  
            price = (strike * np.exp(-rate_local * maturity) * norm.cdf(-d2) -
                    spot * np.exp((adjusted_rate - rate_local) * maturity) * norm.cdf(-d1))
        
        return price




    def black_scholes_up_probability(spot, barrier, time, rate, dividend_yield, volatility):
     
        if barrier <= 0:
            return 1.0
        if time <= 0:
            return 1.0 if spot >= barrier else 0.0
        
        d2 = (
            np.log(spot / barrier) 
            + (rate - dividend_yield - 0.5 * volatility**2) * time
        ) / (volatility * np.sqrt(time))
        
        return norm.cdf(d2)




