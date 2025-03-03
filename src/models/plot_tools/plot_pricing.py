

# plot_pricing.py

import numpy as np
import plotly.graph_objects as go
import copy

from models.option_models.asian_option import AsianOption
from models.option_models.vanilla_option import VanillaOption
from models.option_models.strategy import OptionStrategy



class OptionGraph:
    def __init__(self, option, price_method = None, payoff_method = None):
        self.option = option
        self.price_method = price_method
        self.payoff_method = payoff_method
        self.strike = option.strike




    def generate_spot_prices(spot, factor=0.8):
        spot_min = max(spot * (1 - factor), 1e-5)
        spot_max = spot * (1 + factor)
        return np.linspace(spot_min, spot_max, 100)




    @staticmethod
    def plot_strategy_payoff(strategy):
        strategy_copy = copy.deepcopy(strategy)
        spot_prices = OptionGraph.generate_spot_prices(strategy.options[0].spot, factor=1.0)
        payoff_values = []

        for new_spot in spot_prices:
            for option in strategy_copy.options:
                option.spot = new_spot
            payoff = OptionStrategy.payoff(strategy_copy)
            payoff_values.append(payoff)

        min_y = min(payoff_values)
        max_y = max(payoff_values)
        range_padding = 0.2 * (max_y - min_y) if max_y != min_y else 1.0  
        new_min_y = min_y - range_padding
        new_max_y = max_y + range_padding

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spot_prices,
            y=payoff_values,
            mode='lines',
            name='Strategy Payoff',
            line=dict(color='#E07D10', width=3) 
        ))

        unique_strikes = sorted(set(option.strike for option in strategy_copy.options))

        strike_colors = ['#00FF00', '#1F77B4', '#800080', '#FF0000', '#FFD700', '#FFFFFF', '#17BECF']
        num_strikes = len(unique_strikes)

        for i, strike in enumerate(unique_strikes):
            color = strike_colors[i % len(strike_colors)]  
            fig.add_trace(go.Scatter(
                x=[strike, strike],
                y=[new_min_y, new_max_y],
                mode='lines',
                line=dict(color=color, dash='dash', width=2),  
                name=f'Strike {i+1}'
            ))

  
        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black',
            title={
                'text': f'{strategy.strategy_type.capitalize()} Payoff',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title='Spot Price',
            yaxis_title='Total Payoff',
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
    def plot_strategy_price(strategy):
        strategy_copy = copy.deepcopy(strategy)
        spot_prices = OptionGraph.generate_spot_prices(strategy.options[0].spot, factor=1.0)
        price_values = []

        for new_spot in spot_prices:
            for option in strategy_copy.options:
                option.spot = new_spot
            price = OptionStrategy.price(strategy_copy)  
            price_values.append(price)


        min_y = min(price_values)
        max_y = max(price_values)
        range_padding = 0.2 * (max_y - min_y) if max_y != min_y else 1.0  
        new_min_y = min_y - range_padding
        new_max_y = max_y + range_padding

        fig = go.Figure()


        fig.add_trace(go.Scatter(
            x=spot_prices,
            y=price_values,
            mode='lines',
            name='Strategy Price',
            line=dict(color='#E07D10', width=3)  
        ))

        unique_strikes = sorted(set(option.strike for option in strategy_copy.options))

        strike_colors = ['#00FF00', '#1F77B4', '#800080', '#FF0000', '#FFD700', '#FFFFFF', '#17BECF']
        num_strikes = len(unique_strikes)

        for i, strike in enumerate(unique_strikes):
            color = strike_colors[i % len(strike_colors)]  
            fig.add_trace(go.Scatter(
                x=[strike, strike],
                y=[new_min_y, new_max_y],
                mode='lines',
                line=dict(color=color, dash='dash', width=2), 
                name=f'Strike {i+1}'
            ))

        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black',
            title={
                'text': f'{strategy.strategy_type.capitalize()} Price',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title='Spot Price',
            yaxis_title='Total Price (Premium)',
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
    def plot_payoff_vs_spot(option, payoff_method, y_axis_label="Payoff"):
        option_copy = copy.deepcopy(option)  
        spot_prices = OptionGraph.generate_spot_prices(option.spot, factor=1.0)
        payoff_values = []

        for spot in spot_prices:
            option_copy.spot = spot
            payoff = payoff_method(option_copy)
            payoff_values.append(payoff)

        min_y = min(payoff_values)
        max_y = max(payoff_values)
        range_padding = 0.2 * (max_y - min_y) if max_y != min_y else 1.0  
        new_min_y = min_y - range_padding
        new_max_y = max_y + range_padding

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spot_prices,
            y=payoff_values,
            mode='lines',
            name=f'{y_axis_label}',
            line=dict(color='#E07D10', width=3)  
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
            'barrier_level': ('#17BECF', 'solid', 'Barrier Level')  
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

        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black',
            title={
                'text': y_axis_label,  
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title='Spot Price',
            yaxis_title=y_axis_label,
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
    def plot_premium_vs_spot(option, price_method, y_axis_label="Premium"):
        option_copy = copy.deepcopy(option)  
        spot_prices = OptionGraph.generate_spot_prices(option.spot, factor=1.0)
        premium_values = []

        for spot in spot_prices:
            option_copy.spot = spot
            premium = price_method(option_copy)
            premium_values.append(premium)

        min_y = min(premium_values)
        max_y = max(premium_values)
        range_padding = 0.2 * (max_y - min_y) if max_y != min_y else 1.0 
        new_min_y = min_y - range_padding
        new_max_y = max_y + range_padding

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=spot_prices,
            y=premium_values,
            mode='lines',
            name=f'{y_axis_label}',
            line=dict(color='#E07D10', width=3) 
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

        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black',  
    
            title={
                'text': y_axis_label,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title='Spot Price',
            yaxis_title=y_axis_label,
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





    
    def create_premium_3d_graph_spot_vol(self, min_spot_factor=0.5, max_spot_factor=1.5, 
                                    min_vol=0.05, max_vol=0.3, spot_steps=50, vol_steps=50):
       
        option_copy = copy.deepcopy(self.option) 

        spot_prices = np.linspace(self.option.strike * min_spot_factor, self.option.strike * max_spot_factor, spot_steps)
        volatilities = np.linspace(min_vol, max_vol, vol_steps)

        spot_grid, vol_grid = np.meshgrid(spot_prices, volatilities)
        premium_values = np.zeros_like(spot_grid)

        for i in range(spot_grid.shape[0]):
            for j in range(spot_grid.shape[1]):
                option_copy.spot = spot_grid[i, j]  
                option_copy.volatility = vol_grid[i, j]  
                premium_values[i, j] = self.price_method(option_copy)  

        fig = go.Figure(data=[go.Surface(z=premium_values, x=spot_grid, y=vol_grid, colorscale='Viridis')])

        fig.update_layout(
            title=f'{type(self.option).__name__} Price vs Spot & Volatility',
            scene=dict(
                xaxis_title='Spot Price',
                yaxis_title='Volatility',
                zaxis_title='Premium (Option Price)'
            ),
            template='plotly_dark'
        )

        return fig

