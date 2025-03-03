

# plotter.py

from models.plot_tools.plot_greeks import GreekPlotter
from models.plot_tools.plot_pricing import OptionGraph

class Plotter:
    def __init__(self, option, price_method = None, greek_method=None, payoff_method = None):
        self.option = option
        self.price_method = price_method
        self.greek_method = greek_method
        self.payoff_method = payoff_method
        self.strike = option.strike



    def payoff(self):
        return OptionGraph.plot_payoff_vs_spot(self.option, self.payoff_method)

    def premium(self):
        return OptionGraph.plot_premium_vs_spot(self.option, self.price_method)

    def delta(self):
        return GreekPlotter.plot_greek_vs_spot(self.option, self.greek_method, 'Delta')



    def gamma(self):
        return GreekPlotter.plot_greek_vs_spot(self.option, self.greek_method, 'Gamma')
    
    def vega(self):
        return GreekPlotter.plot_greek_vs_spot(self.option, self.greek_method, 'Vega')
    
    def theta(self):
        return GreekPlotter.plot_greek_vs_spot(self.option, self.greek_method, 'Theta')
    
    def rho(self):
        return GreekPlotter.plot_greek_vs_spot(self.option, self.greek_method, 'Rho')