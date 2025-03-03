

#monte_carlo.py

import numpy as np
import pandas as pd

from models.pricing_method.black_scholes import BlackScholesPricer

class MonteCarloPricer:

    @staticmethod
    def simulate_gbm_euler(S, T, r, sigma, q, num_paths, time_steps, seed=None):
        if seed is not None:
            np.random.seed(seed)

        dt = T / time_steps
        dW = np.random.randn(num_paths, time_steps) * np.sqrt(dt)
        
        log_increments = (r - q - 0.5 * sigma**2) * dt + sigma * dW
        log_S = np.cumsum(log_increments, axis=1) 
        log_S = np.log(np.maximum(S, 1e-8)) + log_S  
        S_paths = np.exp(log_S) 
        
        S_paths = np.hstack((np.full((num_paths, 1), S), S_paths))
        
        return S_paths, dW

    @staticmethod
    def price_barrier(
        type_option, spot, strike, maturity, rate, volatility, dividend_yield,
        barrier_level, barrier_type, rebate=0.0,
        num_paths=500000, time_steps=200, seed=None):

        if barrier_type == 'up-and-out' and spot >= barrier_level:
            return rebate  
        elif barrier_type == 'down-and-out' and spot <= barrier_level:
            return rebate


        S_paths, _ = MonteCarloPricer.simulate_gbm_euler(
            S=spot, T=maturity, r=rate, sigma=volatility, q=dividend_yield,
            num_paths=num_paths, time_steps=time_steps, seed=seed)
        
        if "up" in barrier_type:
            crossed = np.any(S_paths >= barrier_level, axis=1)
        else:  
            crossed = np.any(S_paths <= barrier_level, axis=1)
        


        final_underlyings = S_paths[:, -1]  

        if "call" in type_option:
            vanilla_payoffs = np.maximum(final_underlyings - strike, 0.0)
        else:  
            vanilla_payoffs = np.maximum(strike - final_underlyings, 0.0)
  
        payoffs = vanilla_payoffs.copy() 
        if "in" in barrier_type:
            payoffs[~crossed] = rebate
        else:
            payoffs[crossed] = rebate

        discounted_payoffs = np.exp(-rate * maturity) * payoffs
        price = np.mean(discounted_payoffs)
        return price

    @staticmethod
    def price_asian(
        type_option, spot, strike, maturity, rate, volatility, dividend_yield,
        average_type, observation_frequency, num_paths = 50000, time_steps=200, seed=None
    ):
    
        if maturity > 1.8:
            time_steps = 500
        
        S_paths, _  = MonteCarloPricer.simulate_gbm_euler(spot, maturity, rate, volatility, dividend_yield, num_paths, time_steps, seed)

        if observation_frequency == 'daily':
            num_observations = round(maturity * 365)
        elif observation_frequency == 'weekly':
            num_observations = round(maturity * 52)
        elif observation_frequency == 'monthly':
            num_observations = round(maturity * 12)
        else:
            raise ValueError("frequency must be 'daily', 'weekly', or 'monthly'.")

        observation_indices = np.linspace(0, time_steps, num_observations, endpoint=False, dtype=int)
        observed_prices = S_paths[:, observation_indices]


        if average_type == "arithmetic":
            averages = np.mean(observed_prices, axis=1)
        elif average_type == "geometric":
            averages = np.exp(np.mean(np.log(observed_prices), axis=1))
        else:
            raise ValueError("average_type must be 'arithmetic' or 'geometric'.")

        # Calcul des payoffs
        if type_option == "call":
            payoffs = np.maximum(averages - strike, 0)
        else:  # put
            payoffs = np.maximum(strike - averages, 0)

        # Actualisation du payoff
        return np.exp(-rate * maturity) * np.mean(payoffs)

    @staticmethod
    def price_lookback(
        type_option, spot, strike, maturity, rate, volatility, dividend_yield,
        strike_type, num_paths=500000, time_steps=200, seed=None):
 

        S_paths, _  = MonteCarloPricer.simulate_gbm_euler(spot, maturity, rate, volatility, dividend_yield, num_paths, time_steps, seed)


        min_S = np.min(S_paths, axis=1)
        max_S = np.max(S_paths, axis=1)
        final_S = S_paths[:, -1]

        if strike_type == "fixed":
            if type_option == "call":
                payoffs = np.maximum(max_S - strike, 0)
            else:  
                payoffs = np.maximum(strike - min_S, 0)
        elif strike_type == "floating":
            if type_option == "call":
                payoffs = np.maximum(final_S - min_S, 0)
            else:  
                payoffs = np.maximum(max_S - final_S, 0)
        else:
            raise ValueError("strike_type must be 'fixed' or 'floating'.")

        return np.exp(-rate * maturity) * np.mean(payoffs)


    def price_autocall(
            spot,     
            maturity,   
            rate,            
            volatility,     
            dividend_yield,  
            coupon,         
            barrier_capital,
            barrier_early,
            barrier_coupon,
            type_autocall='phoenix', 
            frequency_per_year='semestrially',
            memory_feature=True,
            barriers_as_percentage=True,
            num_paths=6000,
            time_steps=250
        ):

        FREQUENCIES = {
            'annually': 1,
            'semestrially': 2,
            'quarterly': 4,
            'monthly': 12
        }



        if type_autocall == 'athena':
            barrier_coupon = barrier_early 


        if barriers_as_percentage:
            barrier_capital_abs = spot * barrier_capital / 100
            barrier_coupon_abs = spot * barrier_coupon / 100
            barrier_early_abs = spot * barrier_early / 100
        else:
            barrier_capital_abs = barrier_capital
            barrier_coupon_abs = barrier_coupon
            barrier_early_abs = barrier_early

        if frequency_per_year not in FREQUENCIES:
            raise ValueError(f"Fréquence non reconnue : {frequency_per_year}. "
                            f"Choisir parmi {list(FREQUENCIES.keys())}.")
        
        
        obs_per_year = FREQUENCIES[frequency_per_year]

        # Nombre total d'observations
        total_observations = int(round(obs_per_year * maturity))

        # Dates d'observation en fraction d'années
        observation_times = [(k+1)/obs_per_year for k in range(total_observations)]

        # Dates d'observation à date step
        observation_indices = [int(round((t_obs*time_steps) / maturity)) for t_obs in observation_times]

        S, _  = MonteCarloPricer.simulate_gbm_euler(spot, maturity, rate, volatility, dividend_yield, num_paths, time_steps, seed=None)

        
            


        def verif_coupon(S, time_to_analyse,observation_indices, histo_coupon, duree_vie, barrier_coupon_abs, maturity, rate, coupon):
        

            obs_idx = observation_indices.index(time_to_analyse)

            for i in range(num_paths):
                if S[i, time_to_analyse] >= barrier_coupon_abs and duree_vie[i] == observation_indices[-1]:

                    histo_coupon[i, obs_idx] = 1


            return histo_coupon
        
   
            

        def verif_remboursement(S, time_to_analyse, resultat, duree_vie, barrier_early_abs, maturity, rate, index):
            
            for i in range(num_paths):
                if S[i, time_to_analyse] >= barrier_early_abs and duree_vie[i] == observation_indices[-1]:

                    resultat[i] = spot * np.exp(rate * (maturity -observation_times[index]))
                    duree_vie[i] = time_to_analyse


            return resultat , duree_vie


        def verif_capital(S, time_to_analyse, resultat, duree_vie, barrier_capital_abs, maturity, rate, index):
            
            nb_crash = 0

            for i in range(len(S)):
                if S[i, time_to_analyse] <= barrier_capital_abs and duree_vie[i] == observation_indices[-1]:

                    resultat[i] = S[i, time_to_analyse] * np.exp(rate * (maturity - observation_times[index]))
                    duree_vie[i] = time_to_analyse
                    nb_crash += 1
                    
            return resultat , duree_vie, nb_crash
            

  
        def memory_app(arr):

            transformed = arr.copy()
            
            for i in range(arr.shape[0]):  
                count = 0  
                
                for j in range(arr.shape[1]):  
                    if arr[i, j] == 1:

                        transformed[i, j] = count + 1
                        count = 0  
                    elif arr[i, j] == 0:
                        count += 1  
            return transformed

    





                
        resultat = np.zeros(num_paths)
        

        duree_vie = np.full(num_paths, observation_indices[-1])


        histo_coupon = np.zeros((num_paths, len(observation_indices)))

        tabl_actualisation = np.zeros(len(observation_indices))
        nb_crash = 0
        count_loss = 0


        i = 0

        for time_to_analyse in observation_indices:

            histo_coupon = verif_coupon(S, time_to_analyse,observation_indices, histo_coupon, duree_vie, barrier_coupon_abs, maturity, rate, coupon)

            resultat, duree_vie = verif_remboursement(S, time_to_analyse, resultat, duree_vie, barrier_early_abs, maturity, rate, i)

            resultat, duree_vie, nb_crash = verif_capital(S, time_to_analyse, resultat, duree_vie, barrier_capital_abs, maturity, rate, i)

            count_loss += nb_crash
            tabl_actualisation[i] = np.exp(rate * (maturity - observation_times[i]))

            i += 1
        

        # Calcul de la matrice de coupon
        if memory_feature:
            histo_coupon = memory_app(histo_coupon)

        tab_coupon = histo_coupon * tabl_actualisation * coupon

        





        



      
        for i in range(len(resultat)):
            if duree_vie[i] == observation_indices[-1] and S[i, -1] >= barrier_capital_abs:
                resultat[i] = spot

            resultat[i] += np.sum(tab_coupon[i,:])


        valeur_actu =(np.mean(resultat) * np.exp(-rate * maturity))






        return valeur_actu


