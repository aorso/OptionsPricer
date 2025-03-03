
# greek_test.py


import copy
import warnings
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import UnivariateSpline

class SmoothedGreek:
    
    @staticmethod
    def generate_param_values(option, param, nb_points=18, factor=1.0):
        if param == "spot":
            spot_min = max(option.spot * (1 - factor), 1e-5)
            spot_max = option.spot * (1 + factor)
            return np.linspace(spot_min, spot_max, nb_points)

        elif param == "vol":
            vol_min = 0.01
            vol_max = 0.8
            return np.linspace(vol_min, vol_max, nb_points)

        elif param == "maturity":
            mat_min = max(option.maturity * (1 - factor), 0.0001)
            mat_max = option.maturity * (1 + factor)
            return np.linspace(mat_min, mat_max, nb_points)

        elif param == "rate":
            rate_min = -0.01
            rate_max = 0.1
            return np.linspace(rate_min, rate_max, nb_points)

        else:
            raise ValueError(f"Paramètre inconnu : {param}")

    @staticmethod
    def compute_optimal_smoothing(price_values, percentage=0.1):
        variance = np.std(price_values)
        smoothing = max(1e-5, percentage * variance)  
        return smoothing

    @staticmethod
    def interpolation(option, price_method, greek_name="premium", nb_points=None, factor=1.0, smoothing=None, percentage=None, title_graph = " "):
        GREEK_INFO = {
            "premium": {"param": "spot", "nb_points": 50, "order": 0, "label": "Prix"},
            "delta": {"param": "spot", "nb_points": 50, "order": 1, "label": "Delta"},
            "gamma": {"param": "spot", "nb_points": 50, "order": 2, "label": "Gamma"},
            "vega": {"param": "vol", "nb_points": 50, "order": 1, "label": "Vega"},
            "theta": {"param": "maturity", "nb_points": 50, "order": 1, "label": "Theta"},
            "rho": {"param": "rate", "nb_points": 50, "order": 1, "label": "Rho"},
        }

        if greek_name not in GREEK_INFO:
            raise ValueError(f"Grecque {greek_name} non supportée.")

        config = GREEK_INFO[greek_name]
        param_to_vary = config["param"]
        derivative_order = config["order"]
        greek_label = config["label"]
        nb_points = config["nb_points"] if nb_points is None else nb_points

        param_values = SmoothedGreek.generate_param_values(option, param_to_vary, nb_points, factor)

        price_list = []
        option_copy = copy.deepcopy(option)

        for val in param_values:
            setattr(option_copy, param_to_vary, val)
            price = price_method(option_copy)
            if np.isnan(price) or np.isinf(price):
                warnings.warn(f"Valeur anormale détectée pour {param_to_vary} = {val}: {price}")
            price_list.append(price)

        if np.std(price_list) < 1e-5:  # Trop peu de variations
            warnings.warn(f"La variation des prix est trop faible pour estimer {greek_name}.")

        if smoothing is None:
            percentage = percentage or 0.1
            smoothing = SmoothedGreek.compute_optimal_smoothing(price_list, percentage)
            print(f"Smoothing automatique calculé : {smoothing:.5f}")

        spline = UnivariateSpline(param_values, price_list, s=smoothing)

        smoothed_y = spline(param_values) if greek_name == "premium" else spline.derivative(derivative_order)(param_values)

        min_y, max_y = min(smoothed_y), max(smoothed_y)
        range_padding = 0.2 * (max_y - min_y) if max_y != min_y else 1.0
        new_min_y, new_max_y = min_y - range_padding, max_y + range_padding

        fig = go.Figure()

        line_color = "#E07D10"  #orange Bloomberg


        fig.add_trace(
            go.Scatter(
                x=param_values,
                y=smoothed_y,
                mode='lines',
                name=f'{title_graph}',
                line=dict(color=line_color, width=3)  
            )
        )


        if param_to_vary == "spot" and hasattr(option, 'strike'):
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
            'barrier_level': ('#17BECF', 'dashdot', 'Barrier Level'),
            'pdi_barrier': ('#FF00FF', 'dashdot', 'PDI Barrier'),  
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
                'text': title_graph,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='white', family='Arial')
            },
            xaxis_title=param_to_vary.capitalize(),
            yaxis_title= title_graph,
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
