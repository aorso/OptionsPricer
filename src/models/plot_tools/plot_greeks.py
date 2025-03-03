
# plot_greeks.py

import copy
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline
 


class GreekPlotter:
    def __init__(self, option, greek_method, nb_points=100):
        self.option = option
        self.greek_method = greek_method
        self.nb_points = nb_points
    
    
    
    
    
    @staticmethod
    def compute_spot_range_for_strategy(strategy, nb_points=100, buffer_percentage=None):
        if not strategy.options:
            raise ValueError("La stratégie ne contient aucune option pour déterminer la plage de spot.")

        # Récupère tous les strikes
        all_strikes = [opt.strike for opt in strategy.options if opt.strike is not None]
        if not all_strikes:
            raise ValueError("Impossible de récupérer les strikes des options de la stratégie.")

        initial_spot = strategy.options[0].spot

        min_strike = min(all_strikes)
        max_strike = max(all_strikes)

        if min_strike <= 0:
            raise ValueError("Le strike minimum doit être positif pour définir une plage de spot.")

        buffer_percentage = 0.9 if buffer_percentage == None else buffer_percentage
        min_spot = max(0, (1 - buffer_percentage) * min_strike)  
        max_spot = (1 + buffer_percentage) * max_strike


        if min_spot >= max_spot:
            raise ValueError("Impossible de définir une plage de spot correcte à partir des strikes fournis.")

        spot_prices = np.linspace(min_spot, max_spot, nb_points)
        return spot_prices



    @staticmethod
    def plot_strategy_greek(strategy, greek_name, nb_points=100):

        strategy_copy = copy.deepcopy(strategy)

        spot_prices = GreekPlotter.compute_spot_range_for_strategy(strategy_copy, nb_points=nb_points)

        greek_values = []
    
        for new_spot in spot_prices:
  
            for opt in strategy_copy.options:
                opt.spot = new_spot

            total_greek_value = strategy_copy.greek().get(greek_name, 0)
            greek_values.append(total_greek_value)


        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spot_prices,
            y=greek_values,
            mode='lines',
            name=f'{greek_name}',
            line=dict(color='#E07D10', width=3), 
        ))


        all_strikes = sorted(set(opt.strike for opt in strategy_copy.options))
        strike_colors = ['#00FF00', '#1F77B4', '#800080', '#FF0000', '#FFD700', '#FFFFFF', '#17BECF']


        min_y = min(greek_values)
        max_y = max(greek_values)
        if np.isclose(min_y, max_y):
            min_y -= 1
            max_y += 1
        else:
            padding_y = 0.2 * (max_y - min_y)
            min_y -= padding_y
            max_y += padding_y

        for i, strike in enumerate(all_strikes):
            color = strike_colors[i % len(strike_colors)]
            fig.add_trace(go.Scatter(
                x=[strike, strike],
                y=[min_y, max_y],
                mode='lines',
                line=dict(color=color, dash='dash', width=2),  
                name=f'Strike={strike}'
            ))


        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black',
            title={
                'text': f"{strategy.strategy_type.capitalize()} {greek_name}",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title='Spot Price',
            yaxis_title=f'{greek_name}',
            yaxis=dict(
                range=[min_y, max_y],
                gridcolor='rgba(255,255,255,0.15)',  
                zerolinecolor='rgba(255,255,255,0.3)', 
                title=dict(font=dict(size=14, color='white', family='Arial')),
                tickfont=dict(size=12, color='white', family='Arial')
            ),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.15)',
                zerolinecolor='rgba(255,255,255,0.3)',
                title=dict(font=dict(size=14, color='white', family='Arial')),
                tickfont=dict(size=12, color='white', family='Arial')
            ),
            legend=dict(
                orientation='v',
                x=1.02,
                y=1,
                font=dict(size=12, color='white', family='Arial'),
                bgcolor='rgba(0,0,0,0)',
                bordercolor='white',
                borderwidth=1
            ),
            hovermode="x"
        )

        return fig


    @staticmethod
    def compute_adaptive_spot_range(spot, strike, nb_points=100):
        if spot <= 0 or strike <= 0:
            raise ValueError("Le spot et le strike doivent être des nombres positifs.")

        buffer_percentage = 1.2  
        min_spot = max(0, (1 - buffer_percentage) * strike)
        max_spot = (1 + buffer_percentage) * strike

       
        near_strike = np.linspace(strike * 0.85, strike * 1.15, int(nb_points * 0.6))
        below_strike = np.linspace(min_spot, strike * 0.85, int(nb_points * 0.2))
        above_strike = np.linspace(strike * 1.15, max_spot, int(nb_points * 0.2))

        spots = np.unique(np.concatenate((below_strike, near_strike, above_strike)))

        return spots


    @staticmethod
    def plot_greek_vs_spot(option, greek_method, greek_name):
        initial_spot = option.spot
        spots = GreekPlotter.compute_adaptive_spot_range(option.spot, option.strike)

        greek_values = []

        option_copy = copy.deepcopy(option)
        for spot in spots:
            option_copy.spot = spot
            greek_value = greek_method(option_copy)[greek_name]
            greek_values.append(greek_value)

        greek_values = np.array(greek_values)
        spots = np.array(spots)

        valid_indices = ~np.isnan(greek_values) & ~np.isinf(greek_values)
        filtered_spots = spots[valid_indices]
        filtered_greek_values = greek_values[valid_indices]

        cleaned_greek_values = filtered_greek_values

        min_y = min(cleaned_greek_values)
        max_y = max(cleaned_greek_values)
        range_padding = 0.2 * (max_y - min_y) if max_y != min_y else 1.0  
        new_min_y = min_y - range_padding
        new_max_y = max_y + range_padding

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered_spots,
            y=cleaned_greek_values,
            mode='lines',
            name=f'{greek_name}',
            line=dict(color='#E07D10', width=3, shape='spline', smoothing=1.3)  
        ))


        fig.add_trace(go.Scatter(
            x=[option.strike, option.strike],
            y=[new_min_y, new_max_y],
            mode='lines',
            line=dict(color='#00FF00', dash='dash', width=2), 
            name='Strike'
        ))

        barrier_types = {
            'barrier': ('#1F77B4', 'dot', 'Barrier'),  
            'protection_barrier': ('#800080', 'dot', 'Protection Barrier'),  
            'barrier_capital': ('#FF0000', 'dashdot', 'Capital Barrier'),  
            'barrier_coupon': ('#FFD700', 'dashdot', 'Coupon Barrier'),  
            'barrier_early': ('#FFFFFF', 'dashdot', 'Early Barrier'),  
            'barrier_level': ('#17BECF', 'dashdot', 'Barrier Level')  
        }

        for barrier_attr, (color, dash, label) in barrier_types.items():
            if hasattr(option, barrier_attr):
                fig.add_trace(go.Scatter(
                    x=[getattr(option, barrier_attr), getattr(option, barrier_attr)],
                    y=[new_min_y, new_max_y],
                    mode='lines',
                    line=dict(color=color, dash=dash, width=2),
                    name=label
                ))

        fig.add_trace(go.Scatter(
            x=[initial_spot, initial_spot],
            y=[new_min_y, new_max_y],
            mode='lines',
            line=dict(color='#FF0000', dash='dash', width=2), 
            name='Spot Initial'
        ))


        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black', 
            title={
                'text': greek_name,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title='Spot Price',
            yaxis_title=greek_name,
            yaxis=dict(
                range=[new_min_y, new_max_y],
                gridcolor='rgba(255,255,255,0.15)',  
                zerolinecolor='rgba(255,255,255,0.3)', 
                title=dict(font=dict(size=14, color='white', family='Arial')),
                tickfont=dict(size=12, color='white', family='Arial')
            ),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.15)',
                zerolinecolor='rgba(255,255,255,0.3)',
                title=dict(font=dict(size=14, color='white', family='Arial')),
                tickfont=dict(size=12, color='white', family='Arial')
            ),
            legend=dict(
                orientation='v',
                x=1.05,
                y=1,
                font=dict(size=12, color='white', family='Arial'),
                bgcolor='rgba(0,0,0,0)',
                bordercolor='white',
                borderwidth=1
            ),
            hovermode="x"
        )

        return fig



    @staticmethod
    def remove_outliers(values, threshold=0.08):

        cleaned_values = values.copy()
        amplitude = np.max(values) - np.min(values)
        
        for i in range(1, len(values) - 1):
            prev_val, curr_val, next_val = values[i - 1], values[i], values[i + 1]
            local_mean = (prev_val + next_val) / 2
           
            if abs(curr_val - local_mean) > threshold * amplitude:
                cleaned_values[i] = local_mean  
        
        return cleaned_values



