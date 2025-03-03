# binomial_tree_greek.py
import math
import numpy as np
from models.pricing_method.binomial_tree import BinomialTreePricer
from concurrent.futures import ThreadPoolExecutor


class BinomialTreeGreek:
    def __init__(self, option):
        self.option = option


    @staticmethod
    def binomial_american_greeks(S, K, T, r, sigma, q, option_type, steps=100, dS_rel=0.05, dSigma_rel=0.05, dR_rel=0.01, dT=1/365):

        params = {"spot": S, "strike": K, "maturity": T, "rate": r, "volatility": sigma, "dividend_yield": q}

        price_0 = BinomialTreePricer.price_vanilla_american(S, K, T, r, sigma, q, option_type, steps, american=True)

        def bumped_price(param_name, bump):
            original_value = params[param_name]
            params[param_name] = original_value + bump
            bumped_price = BinomialTreePricer.price_vanilla_american(
                params["spot"], params["strike"], params["maturity"], params["rate"], params["volatility"],
                params["dividend_yield"], option_type, steps, american=True
            )
            params[param_name] = original_value  
            return bumped_price

        dS = max(S * dS_rel, 1e-4)
        delta = (bumped_price("spot", dS) - bumped_price("spot", -dS)) / (2 * dS)
        gamma = (bumped_price("spot", dS) - 2 * price_0 + bumped_price("spot", -dS)) / (dS ** 2)

        dSigma = max(sigma * dSigma_rel, 1e-4)
        vega = (bumped_price("volatility", dSigma) - price_0) / dSigma

        dR = r * dR_rel
        rho = (bumped_price("rate", dR) - price_0) / dR

        price_T_down = bumped_price("maturity", -dT)
        theta = (price_T_down - price_0) / (dT)

        return {
            "Delta": float(delta),
            "Gamma": float(gamma), 
            "Vega": float(vega),
            "Theta": float(theta),
            "Rho": float(rho),
        }



    @staticmethod
    def binomial_barrier_greeks(S, K, T, r, sigma, q, option_type, barrier_level, barrier_type, rebate=0, steps=60, dS_rel=0.1, dSigma_rel=0.1, dR_rel=0.01, dT=1/365):
    
        params = {
            "spot": S,
            "strike": K,
            "maturity": T,
            "rate": r,
            "volatility": sigma,
            "dividend_yield": q,
            "barrier_level": barrier_level,
            "barrier_type": barrier_type,
            "rebate": rebate
        }


        price_0 = BinomialTreePricer.price_barrier_binomial(option_type, S, K, T, r, sigma, q, barrier_level, barrier_type, rebate, steps)
        
        def bumped_price(param_name, bump):
            original_value = params[param_name]
            params[param_name] = original_value + bump
            bumped_price = BinomialTreePricer.price_barrier_binomial(
                option_type,
                params["spot"], params["strike"], params["maturity"], params["rate"],
                params["volatility"], params["dividend_yield"],
                params["barrier_level"], params["barrier_type"], params["rebate"],
                steps
            )
            params[param_name] = original_value  
            return bumped_price


        dS = max(S * dS_rel, 1e-2)
        delta = (bumped_price("spot", dS) - bumped_price("spot", -dS)) / (2 * dS)
        gamma = (bumped_price("spot", dS) - 2 * price_0 + bumped_price("spot", -dS)) / (dS ** 2)
        
        dSigma = sigma * dSigma_rel
        vega = (bumped_price("volatility", dSigma) - price_0) / dSigma
        
        dR = max(r * dR_rel, 1e-2)

        rho = (bumped_price("rate", dR) - price_0) / dR
        
        price_T_down = bumped_price("maturity", -dT)
        theta = (price_T_down - price_0) / (-dT)


        def is_knocked_out(spot, barrier_level, barrier_type):
            if (barrier_type == "up-and-out" and spot >= barrier_level) or (barrier_type == "down-and-out" and spot <= barrier_level):
                return True
            return False
        
        if is_knocked_out(S, barrier_level, barrier_type):
            delta = 0.0
            gamma = 0.0
            vega = 0.0
            theta = 0.0
            rho = 0.0

        return {
            "Delta": float(delta),
            "Gamma": float(gamma),
            "Vega": float(vega),
            "Theta": float(theta),
            "Rho": float(rho),
        }


   