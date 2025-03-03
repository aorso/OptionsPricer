
#binomial_tree.py

import math
import numpy as np

class BinomialTreePricer:
    @staticmethod
    def price_vanilla_american(S, K, T, r, sigma, q=0, option_type="call", steps=500, american=False): 
        dt = T / steps
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        p = (math.exp((r - q) * dt) - d) / (u - d)

        if not (0 <= p <= 1):
            raise ValueError(f"Probabilité neutre au risque invalide : p={p}")

        prices = np.zeros((steps + 1, steps + 1))
        prices[0, 0] = S

        for i in range(1, steps + 1):
            prices[i, 0] = prices[i-1, 0] * u
            for j in range(1, i + 1):
                prices[i, j] = prices[i-1, j-1] * d

        option_values = np.zeros((steps + 1, steps + 1))
        for j in range(steps + 1):
            if option_type == "call":
                option_values[steps, j] = max(0, prices[steps, j] - K)
            elif option_type == "put":
                option_values[steps, j] = max(0, K - prices[steps, j])

        for i in range(steps - 1, -1, -1):
            for j in range(i + 1):
                continuation_value = math.exp(-r * dt) * (p * option_values[i+1, j] + (1 - p) * option_values[i+1, j+1])
                if option_type == "call":
                    intrinsic_value = max(0, prices[i, j] - K)
                else:  # put
                    intrinsic_value = max(0, K - prices[i, j])

                if american:
                    option_values[i, j] = max(continuation_value, intrinsic_value)
                else:
                    option_values[i, j] = continuation_value

        return option_values[0, 0]

    @staticmethod
    def price_barrier_binomial(
        type_option, spot, strike, maturity, rate, volatility, dividend_yield,
        barrier_level, barrier_type, rebate=0.0,
        steps=200):

        dt = maturity / steps
        u = np.exp(volatility * np.sqrt(dt))  
        d = 1 / u                    
        p = (np.exp((rate - dividend_yield) * dt) - d) / (u - d)  
        
        prices = np.zeros((steps + 1, steps + 1))
        prices[0, 0] = spot

        for i in range(1, steps + 1):
            for j in range(i + 1):
                prices[j, i] = spot * (u ** (i - j)) * (d ** j)

        payoffs = np.zeros(steps + 1)
        if "call" in type_option:
            payoffs = np.maximum(prices[:, steps] - strike, 0.0)
        else:
            payoffs = np.maximum(strike - prices[:, steps], 0.0)

        for i in range(steps - 1, -1, -1):
            for j in range(i + 1):

                payoffs[j] = np.exp(-rate * dt) * (p * payoffs[j] + (1 - p) * payoffs[j + 1])


                if "up" in barrier_type and prices[j, i] >= barrier_level:
                    if "in" in barrier_type:
                        payoffs[j] = payoffs[j]  
                    else:
                        payoffs[j] = rebate  
                        
                elif "down" in barrier_type and prices[j, i] <= barrier_level:
                    if "in" in barrier_type:
                        payoffs[j] = payoffs[j] 
                    else:
                        payoffs[j] = rebate  

        return payoffs[0]



    @staticmethod
    def _calculate_observation_dates(maturity, frequency, steps):

        frequency_map = {
            'annual': 1,
            'semi-annual': 2,
            'quarterly': 4,
            'monthly': 12
        }
        
        if isinstance(frequency, str):
            frequency = frequency.strip("'") 
            
        if frequency not in frequency_map:
            raise ValueError(f"Invalid frequency: {frequency}. Choose from 'annual', 'semi-annual', 'quarterly', 'monthly'.")
        
        observations_per_year = frequency_map[frequency]
        total_observations = int(maturity * observations_per_year)
        
        if total_observations == 0:
            return [steps]  
            
        dt = maturity / steps
        observation_dates = []
        
        for i in range(1, total_observations + 1):
            t = i * (maturity / total_observations)
            idx = min(steps, int(round(t / dt)))
            observation_dates.append(idx)
            
        return sorted(set(observation_dates))
    


    




