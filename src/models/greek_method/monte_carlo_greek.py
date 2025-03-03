# monte_carlo_greek.py
import numpy as np
import pandas as pd
from models.pricing_method.monte_carlo import MonteCarloPricer

class MonteCarloGreek:
    def __init__(self, option):
        self.option = option

    @staticmethod
    def montecarlo_asian_greeks(type_option, spot, strike, maturity, rate, volatility, dividend_yield, average_type, observation_frequency, num_paths=100_000, time_steps=100, seed=None):
        S_paths, W_shocks = MonteCarloPricer.simulate_gbm_euler(
            S=spot, T=maturity, r=rate, sigma=volatility, q=dividend_yield,
            num_paths=num_paths, time_steps=time_steps, seed=seed
        )
        
        dt = maturity / time_steps
        discount_factor = np.exp(-rate * maturity)

        if observation_frequency == 'daily':
            num_obs = round(maturity * 365)
        elif observation_frequency == 'weekly':
            num_obs = round(maturity * 52)
        elif observation_frequency == 'monthly':
            num_obs = round(maturity * 12)
        else:
            raise ValueError("La fréquence doit être 'daily', 'weekly', ou 'monthly'.")
        num_obs = min(num_obs, time_steps)
        obs_indices = np.linspace(0, time_steps, num_obs, endpoint=False, dtype=int)
        observed_prices = S_paths[:, obs_indices]

        if average_type == "arithmetic":
            avg_values = np.mean(observed_prices, axis=1)
        else:  # "geometric"
            avg_values = np.exp(np.mean(np.log(observed_prices), axis=1))

        intrinsic_payoff = np.maximum(avg_values - strike, 0.0) if type_option == "call" else np.maximum(strike - avg_values, 0.0)
        payoff = discount_factor * intrinsic_payoff

        partial_avg = (
            np.sum(observed_prices / spot, axis=1) / observed_prices.shape[1]
            if average_type == "arithmetic" else avg_values / spot
        )
        indicator_itm = (intrinsic_payoff > 0).astype(float)
        delta_samples = discount_factor * indicator_itm * (partial_avg if type_option == "call" else -partial_avg)
        delta = np.mean(delta_samples)

        sum_W = np.sum(W_shocks, axis=1)
        vega_samples = payoff * (sum_W / volatility - volatility * maturity)
        vega = np.mean(vega_samples)

        theta_score = ((sum_W * (rate - dividend_yield - 0.5 * volatility**2) / volatility**2) - (rate * maturity / volatility))
        theta_samples = payoff * theta_score
        theta = -np.mean(theta_samples)

        rho_samples = payoff * maturity
        rho = np.mean(rho_samples)

        gamma_samples = -discount_factor * indicator_itm * (avg_values / (spot ** 2))
        gamma = np.mean(gamma_samples)

        return {
            "Delta": float(delta),
            "Gamma": float(gamma),
            "Vega": float(vega),
            "Theta": float(theta),
            "Rho": float(rho),
        }






    @staticmethod
    def montecarlo_lookback_greeks(type_option, spot, strike, maturity, rate, volatility, dividend_yield, strike_type, num_paths=6000, time_steps=40, seed=None):

        S_paths, dW = MonteCarloPricer.simulate_gbm_euler(
            S=spot, T=maturity, r=rate, sigma=volatility, q=dividend_yield,
            num_paths=num_paths, time_steps=time_steps, seed=seed)

        dt = maturity / time_steps
        discount = np.exp(-rate * maturity)


        if strike_type == 'floating':
            observed_extreme = np.min(S_paths, axis=1) if type_option == 'call' else np.max(S_paths, axis=1)
            strike = observed_extreme
        else:
            strike = strike

        # payoff
        payoff_intrinsic = np.maximum(S_paths[:, -1] - strike, 0.0) if type_option == 'call' else np.maximum(strike - S_paths[:, -1], 0.0)
        payoff = discount * payoff_intrinsic

        # delta (pathwise)
        delta_pathwise = discount * ((S_paths[:, -1] > strike).astype(float) * (S_paths[:, -1] / np.maximum(spot, 1e-8)))
        Delta = np.mean(delta_pathwise)

        # vega (likelihood ratio)
        normalized_sum_dW = np.sum(dW, axis=1) / np.sqrt(time_steps)
        likelihood_vega = (normalized_sum_dW / volatility) - volatility * maturity
        Vega = np.mean(payoff * likelihood_vega)

        # Theta (likelihood ratio)
        theta_score = np.where(volatility > 1e-6, 
                      (normalized_sum_dW * (rate - dividend_yield - 0.5 * volatility**2) / volatility**2) - (rate * maturity / volatility), 
                      0.0)
        Theta = -np.mean(payoff * theta_score)

        # rho (pathwise)
        rho_samples = payoff * maturity
        Rho = np.mean(rho_samples)

        # Gamma (pathwise)
        gamma_pathwise = -discount * ((payoff_intrinsic / (np.maximum(spot, 1e-8) ** 2)))
        Gamma = np.mean(gamma_pathwise)

        return {
            "Delta": float(Delta),
            "Gamma": float(Gamma),
            "Vega": float(Vega),
            "Theta": float(Theta),
            "Rho": float(Rho),
        }





    def proba_autocall(
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
            time_steps=250 ):

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
        

        if memory_feature:
            histo_coupon = memory_app(histo_coupon)
    


        # Probabilité de choper coupon
        proba_coupon = np.sum(histo_coupon, axis=0)
        proba_coupon = proba_coupon / num_paths

        #Probabilité de survie
        unique, counts = np.unique(duree_vie, return_counts=True)
        maturity_proba = counts / num_paths

        tab_probability_distribution = pd.DataFrame({
            'Maturity Prob.': (maturity_proba * 100).round(2).astype(str) + " %",
            'Coupon Prob.': (proba_coupon * 100).round(2).astype(str) + " %"
        }, index=observation_times)
        
        tab_probability_distribution.index.name = 'Obs.'

        # Maturité espérée
        df =  maturity_proba * observation_times       
        except_maturity = df.sum()

        # Forward à maturité
        forward_at_maturity = spot * np.exp((rate-dividend_yield) * (maturity))

        # Probabilité de perte en capital
        prob_loss = count_loss / num_paths

    
        tab_info2 = pd.DataFrame({
            'Forward at maturity': [forward_at_maturity],
            'Expected maturity': [except_maturity],
            'Capital loss Probability':  [f"{round(prob_loss * 100, 2)} %"]

        }, index=["Value"])  

        return tab_probability_distribution, tab_info2
