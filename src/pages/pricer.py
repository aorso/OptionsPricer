

# pricer.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from functools import partial


from models.option_models import (
    VanillaOption, AsianOption, BarrierOption, DigitOption, 
    LookbackOption, QuantoOption, AutoCallOption, OptionStrategy
)




from models.plot_tools import Plotter, SmoothedGreek, OptionGraph, GreekPlotter


option_data = {
    ("Vanilla Options", "European Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Interest Rate", "Volatility"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]} 
            }
        },
        "type_exercise" : 'European',
        "class": VanillaOption,
        "payoff_function": VanillaOption.payoff,
        "pricing_function": VanillaOption.price,
        "greek_function": VanillaOption.greek,

        "graph_price": {"function": Plotter, "add_parameters": {}}, 
        "graph_payoff": {"function": Plotter, "add_parameters": {}},
        "graph_delta": {"function": Plotter, "add_parameters": {}},
        "graph_gamma": {"function": Plotter, "add_parameters": {}},
        "graph_theta": {"function": Plotter, "add_parameters": {}},
        "graph_rho": {"function": Plotter, "add_parameters": {}},
        "graph_vega": {"function": Plotter, "add_parameters": {}},




        "default_values": {
            "Option type": "Call", "Spot": 100, "Strike": 120, "Maturity Value": 1, "Maturity Unit": "years", 
            "Volatility": 20, "Interest Rate": 5, "Dividend Yield": 3.5
        },
        "variable_mapping": {  
            "Option type": "type_option",  
            "Spot": "spot",
            "Strike": "strike",
            "Maturity Value": "maturity",
            "Maturity Unit": "time_type",
            "Interest Rate": "rate",
            "Volatility": "volatility",
            "Dividend Yield": "dividend_yield"
        },
        "variable_units": {  
            "Volatility": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
    }
    },

    ("Vanilla Options", "American Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Interest Rate", "Volatility"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]} 
            }
        },
        "type_exercise" : 'American',
        "class": VanillaOption,
        "pricing_function": VanillaOption.price,
        "payoff_function": None,
        "greek_function": VanillaOption.greek,

        "graph_price": {"function": Plotter, "add_parameters": {}}, 
        "graph_delta": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points": 70, "percentage": 0.001, "title_graph": "Delta"}},
        "graph_gamma": {"function": SmoothedGreek.interpolation, "add_parameters": {'nb_points': 70, 'percentage': 0.001, "title_graph": "Gamma"}},
        "graph_theta": {"function": SmoothedGreek.interpolation, "add_parameters": {'nb_points' : 70, 'percentage' : 0.5, "title_graph": "Theta"}},
        "graph_rho": {"function": SmoothedGreek.interpolation, "add_parameters": {'nb_points' : 70,'percentage' : 0.01, 'factor' : 1.3, "title_graph": "Rho"}},
        "graph_vega": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 70, "percentage"  : 3, "title_graph": "Vega"}},

        "default_values": {
            "Option type": "Call", "Spot": 100, "Strike": 120, "Maturity Value": 1, "Maturity Unit": "years",
            "Volatility": 20, "Interest Rate": 5, "Dividend Yield": 3.5
        },
            "variable_mapping": {  
                "Option type": "type_option",  
                "Spot": "spot",
                "Strike": "strike",
                "Maturity Value": "maturity",
                "Maturity Unit": "time_type",
                "Interest Rate": "rate",
                "Volatility": "volatility",
                "Dividend Yield": "dividend_yield"
        },
        "variable_units": {  
            "Volatility": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
        }
    },
    

    ("Exotic Options", "Asian Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]},
                    "Average Type": {"choices": ["Arithmetic", "Geometric"]},
                    "Observation Frequency": {"choices": ["Daily", "Weekly", "Monthly"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Interest Rate", "Volatility"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]} 
            }
        },

        "class": AsianOption,
        "payoff_function": None,
        "pricing_function": AsianOption.price,
        "greek_function": AsianOption.greek,
 
        "graph_price": {"function": Plotter, "add_parameters": {}}, 
        "graph_delta": {"function": Plotter, "add_parameters": {}},
        "graph_gamma": {"function": Plotter, "add_parameters": {}},
        "graph_theta": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 50, "percentage"  : 5, "factor" : 0.5}},
        "graph_rho": {"function": Plotter, "add_parameters": {}},
        "graph_vega": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 50, "percentage"  : 5, "factor" : 0.5}},



        "default_values": {
            "Option type": "Call", "Spot": 150, "Strike": 165, "Maturity Value": 1, "Maturity Unit": "years",
            "Volatility": 20, "Interest Rate": 2, "Dividend Yield": 3.5, "Average Type": "arithmetic" ,"Observation Frequency" : "daily"
        },
            "variable_mapping": {  
                "Option type": "type_option",  
                "Spot": "spot",
                "Strike": "strike",
                "Maturity Value": "maturity",
                "Maturity Unit": "time_type",
                "Interest Rate": "rate",
                "Volatility": "volatility",
                "Dividend Yield": "dividend_yield",
                "Average Type": "average_type",
                "Observation Frequency": "observation_frequency",
        },
        "variable_units": {  
            "Volatility": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
    }},
    
    ("Exotic Options", "Barrier Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]},
                    "Barrier Type": {"choices": ["Down-and-In", "Down-and-Out", "Up-and-In", "Up-and-Out"]},
                    "Exercice Type": {"choices": ["European", "American"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Interest Rate", "Volatility"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]} ,
                "Rebate": None,
                "Barrier Level": None
            }
        },
        "class": BarrierOption,
        "payoff_function": BarrierOption.payoff,
        "pricing_function": BarrierOption.price,
        "greek_function": BarrierOption.greek,

        
        "default_values": {
            "Option type": "Call", "Spot": 100, "Strike": 120, "Maturity Value": 1, "Maturity Unit": "years", 
            "Volatility": 20, "Interest Rate": 5, "Dividend Yield": 3.5, "Barrier Type": "Down-and-In", "Exercice Type": "European", "Rebate": 0, "Barrier Level": 150
        },
        "variable_mapping": {  
            "Option type": "type_option",  
            "Spot": "spot",
            "Strike": "strike",
            "Maturity Value": "maturity",
            "Maturity Unit": "time_type",
            "Interest Rate": "rate",
            "Volatility": "volatility",
            "Dividend Yield": "dividend_yield",
            "Barrier Type": "barrier_type",
            "Exercice Type": "type_exercise",
            "Rebate": "rebate",
            "Barrier Level": "barrier_level"
        },
        "variable_units": {  
            "Volatility": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
    },

        "graph_variables": {
            "european": {
                "payoff_function": None,
                "graph_price": {"function": Plotter, "add_parameters": {}},
                "graph_payoff": {"function": Plotter, "add_parameters": {}}, 
                "graph_delta": {"function": Plotter, "add_parameters": {}},
                "graph_gamma": {"function": Plotter, "add_parameters": {}},
                "graph_theta": {"function": Plotter, "add_parameters": {}},
                "graph_rho": {"function": Plotter, "add_parameters": {}},
                "graph_vega": {"function": Plotter, "add_parameters": {}},
                    },
            "american": {
                "graph_price": {"function": Plotter, "add_parameters": {}}, 
                "graph_delta": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 70, "percentage"  : 0.01}},
                "graph_gamma": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 100, "percentage"  : 0.1}},
                "graph_theta": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 70, "percentage"  : 0.5}},
                "graph_rho": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 50, "percentage"  : 0.001, "factor" : 0.5}},
            }
        }},


    ("Exotic Options", "Lookback Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]},
                    "Strike Type": {"choices": ["Fixed", "Floating"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Interest Rate", "Volatility"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]} 
            }
        },
        "class": LookbackOption,
        "payoff_function": None,
        "pricing_function": LookbackOption.price,
        "greek_function": LookbackOption.greek,

        
        "default_values": {
            "Option type": "Call", "Spot": 100, "Strike": 115, "Maturity Value": 1, "Maturity Unit": "years", 
            "Volatility": 20, "Interest Rate": 5, "Dividend Yield": 3.5, "Strike Type": "Fixed"
        },
        "variable_mapping": {  
            "Option type": "type_option",  
            "Spot": "spot",
            "Strike": "strike",
            "Maturity Value": "maturity",
            "Maturity Unit": "time_type",
            "Interest Rate": "rate",
            "Volatility": "volatility",
            "Dividend Yield": "dividend_yield",
            "Strike Type": "strike_type"},

        "variable_units": {  
            "Volatility": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"},

        "graph_variables": {
            "fixed": {
                "graph_price": {"function": Plotter, "add_parameters": {}},
                "graph_delta": {"function": Plotter, "add_parameters": {}},
                "graph_gamma": {"function": Plotter, "add_parameters": {}},
                "graph_theta": {"function": Plotter, "add_parameters": {}},
                "graph_rho": {"function": Plotter, "add_parameters": {}},
                    },
            "floating": {
                "graph_price": {"function": Plotter, "add_parameters": {}} 
            }
        }},

    

    ("Exotic Options", "Quanto Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Volatility",  "Local Rate", "Foreign Rate", "FX Volatility", "FX Correlation"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]} 
            }
        },
        "class": QuantoOption,
        "payoff_function": QuantoOption.payoff,
        "pricing_function": QuantoOption.price,
        "greek_function": QuantoOption.greek,

        "graph_price": {"function": Plotter, "add_parameters": {}}, 
        "graph_payoff": {"function": Plotter, "add_parameters": {}},
        "graph_delta": {"function": Plotter, "add_parameters": {}},
        "graph_gamma": {"function": Plotter, "add_parameters": {}},
        "graph_theta": {"function": Plotter, "add_parameters": {}},
        "graph_rho": {"function": Plotter, "add_parameters": {}},
        "graph_vega": {"function": Plotter, "add_parameters": {}},





        "default_values": {
            "Option type": "Call", "Spot": 100, "Strike": 120, "Maturity Value": 1, "Maturity Unit": "years",
            "Volatility": 20, "Dividend Yield": 10, "Local Rate": 5, "Foreign Rate": 2, "FX Volatility": 5, "FX Correlation": 0.5
        },
            "variable_mapping": {  
                "Option type": "type_option",  
                "Spot": "spot",
                "Strike": "strike",
                "Maturity Value": "maturity",
                "Maturity Unit": "time_type",
                "Volatility": "volatility",
                "Dividend Yield": "dividend_yield",
                "Local Rate": "rate_local",
                "Foreign Rate": "rate_foreign",
                "FX Volatility": "vol_fx",
                "FX Correlation": "fx_correlation"
        },    
        "variable_units": {  
            "Volatility": "%",
            "Dividend Yield": "%",
            "Local Rate": "%",
            "Foreign Rate": "%",
            "FX Volatility": "%"
    }
    },


    ("Autocall", "Phoenix"): {
        "variables": {
            "Market": ["Spot", "Dividend Yield", "Volatility",  "Interest Rate"],
            "Contract": {
                "Coupon" : None,
                "Memory Feature": {"choices": [True, False]},
                "Frequency Observation" : {"choices":  ["Monthly", "Quartly", "Semestrially", "Annually"]},
                "Maturity in years": None,  
            },
            "Barriers": {
                "Autocall Barrier": None,  
                "Coupon Barrier": None, 
                "Protection Barrier": None,
                "Barriers as Percentage": {"choices": [True, False]},
            },
        },

            "variable_mapping": { 
                "Spot": "spot",
                "Maturity in years": "maturity",
                "Interest Rate": "rate",
                "Volatility": "volatility",
                "Dividend Yield": "dividend_yield",
                "Coupon": "coupon",
                "Protection Barrier": "barrier_capital",
                "Coupon Barrier": "barrier_coupon",
                "Autocall Barrier": "barrier_early",
                "Barriers as Percentage": "barriers_as_percentage",
                "Memory Feature": "memory_feature",
                "Frequency Observation": "frequency_per_year"  
        },  

        "type_autocall" : "phoenix",
        "class": AutoCallOption,
        "payoff_function": None,
        "pricing_function": AutoCallOption.price,
        "greek_function": AutoCallOption.prob_tab,

        "graph_price": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 70,  "percentage"  : 0.1}},


        "default_values": {
            "Spot": 100,  "Maturity in years": 5, "Protection Barrier": 65, "Coupon Barrier": 95, "Autocall Barrier": 140, 
            "Coupon": 10, "Volatility": 20, "Dividend Yield": 3.5, "Interest Rate": 2, "Barriers as Percentage": False, "Memory Feature": False, "Frequency Observation": "Semestrially"
            },
  
        "variable_units": {  
            "Volatility": "%",
            "Dividend Yield": "%",
            "Interest Rate": "%"
    }
    },


    ("Autocall", "Athena"): {
        "variables": {
            "Market": ["Spot", "Dividend Yield", "Volatility",  "Interest Rate"],
            "Contract": {
                "Coupon" : None,
                "Memory Feature": {"choices": [True, False]},
                "Frequency Observation" : {"choices":  ["Monthly", "Quartly", "Semestrially", "Annually"]},
                "Maturity in years": None,  
            },
            "Barriers": {
                "Autocall/Coupon Barrier": None,
                "Protection Barrier": None,  
                "Barriers as Percentage": {"choices": [True, False]},
            }
        },

            "variable_mapping": { 
                "Spot": "spot",
                "Maturity in years": "maturity",
                "Interest Rate": "rate",
                "Volatility": "volatility",
                "Dividend Yield": "dividend_yield",
                "Coupon": "coupon",
                "Protection Barrier": "barrier_capital",
                "Autocall/Coupon Barrier":  "barrier_early",

                "Barriers as Percentage": "barriers_as_percentage",
                "Memory Feature": "memory_feature",
                "Frequency Observation": "frequency_per_year"  
        },  

        "type_autocall" : "athena",
        "class": AutoCallOption,
        "payoff_function": None,
        "pricing_function": AutoCallOption.price,
        "greek_function": AutoCallOption.prob_tab,

        "graph_price": {"function": SmoothedGreek.interpolation, "add_parameters": {"nb_points" : 70, "percentage"  : 0.1}},


        "default_values": {
            "Spot": 100,  "Maturity in years": 5, "Protection Barrier": 70,  "Autocall/Coupon Barrier": 130, 
            "Coupon": 10, "Volatility": 20, "Dividend Yield": 3.5, "Interest Rate": 2, "Barriers as Percentage": False, "Memory Feature": False, "Frequency Observation": "Semestrially"
            },
  
        "variable_units": {  
            "Volatility": "%",
            "Dividend Yield": "%",
            "Interest Rate": "%"
    }
    },


    ("Exotic Options", "Digital Option"): {
        "variables": {
            "Option type": {
                "sub_category": {
                    "Option type": {"choices": ["Call", "Put"]}
                }
            },
            "Market": ["Spot", "Dividend Yield", "Interest Rate", "Volatility"],
            "Contract": {
                "Strike": None,  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]},
                "Cash Payout": None
            }
        },
        "class": DigitOption,
        "payoff_function": DigitOption.payoff,
        "pricing_function": DigitOption.price,
        "greek_function": DigitOption.greek,
        
        "graph_price": {"function": Plotter, "add_parameters": {}},
        "graph_payoff": {"function": Plotter, "add_parameters": {}},
        "graph_delta": {"function": Plotter, "add_parameters": {}},
        "graph_gamma": {"function": Plotter, "add_parameters": {}},
        "graph_theta": {"function": Plotter, "add_parameters": {}},
        "graph_rho": {"function": Plotter, "add_parameters": {}},
        "graph_vega": {"function": Plotter, "add_parameters": {}},
                
        "default_values": {
            "Option type": "Call", "Spot": 100, "Strike": 120, "Maturity Value": 1, "Maturity Unit": "years",
            "Volatility": 20, "Interest Rate": 5, "Dividend Yield": 3, "Cash Payout" : 1
        },
            "variable_mapping": {  
                "Option type": "type_option",  
                "Spot": "spot",
                "Strike": "strike",
                "Maturity Value": "maturity",
                "Maturity Unit": "time_type",
                "Interest Rate": "rate",
                "Volatility": "volatility",
                "Dividend Yield": "dividend_yield",
                "Cash Payout": "cash_payout"
        },
        "variable_units": {  
            "Volatility": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
    }
    },

   
    ("Option Strategies", "Call Spread"): {
        "variables": {
            "Call n°1 (Long)": {"Strike 1": None, "Volatility 1": None},
            "Call n°2 (Short)": {"Strike 2": None, "Volatility 2": None},
            "Market": ["Spot", "Interest Rate", "Dividend Yield"],
            "Contract": {  
                "Maturity Value": None,  
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
        },

         },
        "strategy_type": "call_spread",
        "class": OptionStrategy,
        "payoff_function": OptionStrategy.payoff,
        "pricing_function": OptionStrategy.price,
        "greek_function": OptionStrategy.greek,
        
        "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
        "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
        "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
                
        "default_values": {
            "Spot": 100, "Strike": 120, "Maturity Value": 1, "Maturity Unit": "years",
            "Interest Rate": 5, "Dividend Yield": 3, "Strike 1": 110, "Volatility 1": 20, "Strike 2": 130, "Volatility 2": 25
        },
        "variable_mapping": {  
            "Option type": "type_option",  
            "Spot": "spot",
            "Maturity Value": "maturity",
            "Maturity Unit": "time_type",
            "Interest Rate": "rate",
            "Strike 1": "strike_1",
            "Strike 2": "strike_2",
            "Volatility 1": "volatility_1",
            "Volatility 2": "volatility_2",
            "Dividend Yield": "dividend_yield",
            "strategy_type": "strategy_type"
        },
        "variable_units": {  
            "Volatility 1": "%",
            "Volatility 2": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
        }
    },


    ("Option Strategies", "Put Spread"): {
    "variables": {
        "Put n°1 (Short)": {"Strike 1": None, "Volatility 1": None},
        "Put n°2 (Long)": {"Strike 2": None, "Volatility 2": None},
        "Market": ["Spot", "Interest Rate", "Dividend Yield"],
        "Contract": {
            "Maturity Value": None,
            "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
        },
    },
    "strategy_type": "put_spread",
    "class": OptionStrategy,
    "payoff_function": OptionStrategy.payoff,
    "pricing_function": OptionStrategy.price,
    "greek_function": OptionStrategy.greek,
    
    "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
    "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
    "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    
    "default_values": {
        "Spot": 100, 
        "Maturity Value": 1, 
        "Maturity Unit": "years",
        "Interest Rate": 5, 
        "Dividend Yield": 3,
        "Strike 1": 70, 
        "Volatility 1": 20, 
        "Strike 2": 90, 
        "Volatility 2": 22
    },
    "variable_mapping": {
        "Spot": "spot",
        "Maturity Value": "maturity",
        "Maturity Unit": "time_type",
        "Interest Rate": "rate",
        "Dividend Yield": "dividend_yield",
        "Strike 1": "strike_1",
        "Strike 2": "strike_2",
        "Volatility 1": "volatility_1",
        "Volatility 2": "volatility_2",
        "strategy_type": "strategy_type"
    },
    "variable_units": {
        "Volatility 1": "%",
        "Volatility 2": "%",
        "Interest Rate": "%",
        "Dividend Yield": "%"
    }
},


    ("Option Strategies", "Straddle"): {
    "variables": {
        "Call n°1 (Long)": {"Strike 1": None, "Volatility 1": None},
        "Put n°1 (Long)":  {"Strike 2": None, "Volatility 2": None},
        "Market": ["Spot", "Interest Rate", "Dividend Yield"],
        "Contract": {
            "Maturity Value": None,
            "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
        },
    },
    "strategy_type": "straddle",
    "class": OptionStrategy,
    "payoff_function": OptionStrategy.payoff,
    "pricing_function": OptionStrategy.price,
    "greek_function": OptionStrategy.greek,
    
    "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
    "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
    "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    
    "default_values": {
        "Spot": 100,
        "Maturity Value": 1,
        "Maturity Unit": "years",
        "Interest Rate": 5,
        "Dividend Yield": 3,
        "Strike 1": 100, 
        "Volatility 1": 20,
        "Strike 2": 100, 
        "Volatility 2": 20
    },
    "variable_mapping": {
        "Spot": "spot",
        "Maturity Value": "maturity",
        "Maturity Unit": "time_type",
        "Interest Rate": "rate",
        "Dividend Yield": "dividend_yield",
        "Strike 1": "strike_1",
        "Strike 2": "strike_2",
        "Volatility 1": "volatility_1",
        "Volatility 2": "volatility_2",
        "strategy_type": "strategy_type"
    },
    "variable_units": {
        "Volatility 1": "%",
        "Volatility 2": "%",
        "Interest Rate": "%",
        "Dividend Yield": "%"
    }
},


    ("Option Strategies", "Strangle"): {
    "variables": {
        "Call n°1 (Long, OTM)": {"Strike 1": None, "Volatility 1": None},
        "Put n°1 (Long, OTM)":  {"Strike 2": None, "Volatility 2": None},
        "Market": ["Spot", "Interest Rate", "Dividend Yield"],
        "Contract": {
            "Maturity Value": None,
            "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
        },
    },
    "strategy_type": "strangle",
    "class": OptionStrategy,
    "payoff_function": OptionStrategy.payoff,
    "pricing_function": OptionStrategy.price,
    "greek_function": OptionStrategy.greek,
    
    "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
    "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
    "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    
    "default_values": {
        "Spot": 100,
        "Maturity Value": 1,
        "Maturity Unit": "years",
        "Interest Rate": 5,
        "Dividend Yield": 3,
        "Strike 1": 110,
        "Volatility 1": 20,
        "Strike 2": 90,
        "Volatility 2": 20
    },
    "variable_mapping": {
        "Spot": "spot",
        "Maturity Value": "maturity",
        "Maturity Unit": "time_type",
        "Interest Rate": "rate",
        "Dividend Yield": "dividend_yield",
        "Strike 1": "strike_1",
        "Strike 2": "strike_2",
        "Volatility 1": "volatility_1",
        "Volatility 2": "volatility_2",
        "strategy_type": "strategy_type"
    },
    "variable_units": {
        "Volatility 1": "%",
        "Volatility 2": "%",
        "Interest Rate": "%",
        "Dividend Yield": "%"
    }
},

    ("Option Strategies", "Risk Reversal"): {
        "variables": {
            "Call n°1 (Long)": {"Strike 1": None, "Volatility 1": None},
            "Put n°1 (Short)":  {"Strike 2": None, "Volatility 2": None},
            "Market": ["Spot", "Interest Rate", "Dividend Yield"],
            "Contract": {
                "Maturity Value": None,
                "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
            },
        },
        "strategy_type": "risk_reversal",
        "class": OptionStrategy,
        "payoff_function": OptionStrategy.payoff,
        "pricing_function": OptionStrategy.price,
        "greek_function": OptionStrategy.greek,
        
        "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
        "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
        "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
        
        "default_values": {
            "Spot": 100,
            "Maturity Value": 1,
            "Maturity Unit": "years",
            "Interest Rate": 5,
            "Dividend Yield": 3,
            "Strike 1": 105,
            "Volatility 1": 20,
            "Strike 2": 95,
            "Volatility 2": 25
        },
        "variable_mapping": {
            "Spot": "spot",
            "Maturity Value": "maturity",
            "Maturity Unit": "time_type",
            "Interest Rate": "rate",
            "Dividend Yield": "dividend_yield",
            "Strike 1": "strike_1",
            "Strike 2": "strike_2",
            "Volatility 1": "volatility_1",
            "Volatility 2": "volatility_2",
            "strategy_type": "strategy_type"
        },
        "variable_units": {
            "Volatility 1": "%",
            "Volatility 2": "%",
            "Interest Rate": "%",
            "Dividend Yield": "%"
        }
    },
    
    ("Option Strategies", "Butterfly Spread"): {
    "variables": {
        "Call n°1 (Long)": {"Strike 1": None, "Volatility 1": None},
        "Call n°2 (Short)": {"Strike 2": None, "Volatility 2": None},
        "Call n°3 (Long)": {"Strike 3": None, "Volatility 3": None},
        "Market": ["Spot", "Interest Rate", "Dividend Yield"],
        "Contract": {
            "Maturity Value": None,
            "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
        },
    },
    "strategy_type": "butterfly",
    "class": OptionStrategy,
    "payoff_function": OptionStrategy.payoff,
    "pricing_function": OptionStrategy.price,
    "greek_function": OptionStrategy.greek,
    
    "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
    "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
    "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    
    "default_values": {
        "Spot": 100,
        "Maturity Value": 1,
        "Maturity Unit": "years",
        "Interest Rate": 5,
        "Dividend Yield": 3,
        "Strike 1": 90,
        "Volatility 1": 20,
        "Strike 2": 100,
        "Volatility 2": 20,
        "Strike 3": 110,
        "Volatility 3": 20
    },
    "variable_mapping": {
        "Spot": "spot",
        "Maturity Value": "maturity",
        "Maturity Unit": "time_type",
        "Interest Rate": "rate",
        "Dividend Yield": "dividend_yield",
        "Strike 1": "strike_1",
        "Strike 2": "strike_2",
        "Strike 3": "strike_3",
        "Volatility 1": "volatility_1",
        "Volatility 2": "volatility_2",
        "Volatility 3": "volatility_3",
        "strategy_type": "strategy_type"
    },
    "variable_units": {
        "Volatility 1": "%",
        "Volatility 2": "%",
        "Volatility 3": "%",
        "Interest Rate": "%",
        "Dividend Yield": "%"
    }
},


    ("Option Strategies", "Condor Spread"): {
    "variables": {
        "Call n°1 (Long)": {"Strike 1": None, "Volatility 1": None},
        "Call n°2 (Short)": {"Strike 2": None, "Volatility 2": None},
        "Call n°3 (Short)": {"Strike 3": None, "Volatility 3": None},
        "Call n°4 (Long)": {"Strike 4": None, "Volatility 4": None},
        "Market": ["Spot", "Interest Rate", "Dividend Yield"],
        "Contract": {
            "Maturity Value": None,
            "Maturity Unit": {"choices": ["days", "weeks", "months", "years"]}
        },
    },
    "strategy_type": "condor",
    "class": OptionStrategy,
    "payoff_function": OptionStrategy.payoff,
    "pricing_function": OptionStrategy.price,
    "greek_function": OptionStrategy.greek,
    
    "graph_price": {"function": OptionGraph.plot_strategy_price, "add_parameters": {}},
    "graph_payoff": {"function": OptionGraph.plot_strategy_payoff, "add_parameters": {}},
    "graph_delta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_gamma": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_theta": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_rho": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    "graph_vega": {"function": GreekPlotter.plot_strategy_greek, "add_parameters": {}},
    
    "default_values": {
        "Spot": 100,
        "Maturity Value": 1,
        "Maturity Unit": "years",
        "Interest Rate": 5,
        "Dividend Yield": 3.5,
        "Strike 1": 70,
        "Volatility 1": 20,
        "Strike 2": 90,
        "Volatility 2": 15,
        "Strike 3": 110,
        "Volatility 3": 25,
        "Strike 4": 140,
        "Volatility 4": 20
    },
    "variable_mapping": {
        "Spot": "spot",
        "Maturity Value": "maturity",
        "Maturity Unit": "time_type",
        "Interest Rate": "rate",
        "Dividend Yield": "dividend_yield",
        "Strike 1": "strike_1",
        "Strike 2": "strike_2",
        "Strike 3": "strike_3",
        "Strike 4": "strike_4",
        "Volatility 1": "volatility_1",
        "Volatility 2": "volatility_2",
        "Volatility 3": "volatility_3",
        "Volatility 4": "volatility_4",
        "strategy_type": "strategy_type"
    },
    "variable_units": {
        "Volatility 1": "%",
        "Volatility 2": "%",
        "Volatility 3": "%",
        "Volatility 4": "%",
        "Interest Rate": "%",
        "Dividend Yield": "%"
    }
},
}




BLOOMBERG_BG = "#000000"
BLOOMBERG_ORANGE = "#E07D10"
BLOOMBERG_BLUE = "#1F77B4"    
BLOOMBERG_YELLOW = "#FFD700"
BLOOMBERG_TEXT = "#FFFFFF"
BORDER_COLOR = "#808080"
BORDER_COLOR2 = "#303030"  


def apply_custom_styles():
    st.markdown(
        f"""
        <style>
            /* --- Arrière-plan général Bloomberg --- */
            body {{
                background-color: {BLOOMBERG_BG};
                color: {BLOOMBERG_TEXT};
            }}
            div.block-container {{
                padding-top: 20px;
            }}

            .title {{
                font-size: 40px;
                font-weight: bold;
                text-align: center;
                color: {BLOOMBERG_ORANGE};
                margin-top: 20px;
                margin-bottom: 20px;
            }}

            /* ---- Barre de menu (catégories principales) ---- */
            .menu-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 40px;
                margin-bottom: 0px;
            }}
            .menu-separator {{
                width: 65%;
                height: 1px;
                background-color: #808080;
                margin-top: 5px;
                margin-bottom: 20px;
                margin: auto;
            }}

            .menu-container a {{
                text-decoration: none;
                color: {BORDER_COLOR};
            }}
            .menu-container a:hover {{
                color: {BLOOMBERG_ORANGE};
            }}
            .menu-item.active {{
                font-weight: bold;
                color: {BLOOMBERG_ORANGE};
                border-bottom: 3px solid {BLOOMBERG_ORANGE};
                padding-bottom: 5px;
            }}

            /* ---- Sous-menu "pills" ---- */
            .pill-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin-bottom: 0px;
                flex-wrap: wrap;
            }}

            .pill {{
                display: inline-flex;
                align-items: center;
                border: 1px solid #555;
                border-radius: 9999px;
                padding: 8px 16px;
                cursor: pointer;
                transition: background-color 0.2s;
                background-color: transparent;
                color: {BLOOMBERG_TEXT};
                text-decoration: none !important;
            }}

            .pill:hover {{
                background-color: #333333;
                color: {BLOOMBERG_TEXT};
            }}

            .pill.selected {{
                background-color: {BLOOMBERG_ORANGE};
                border-color: {BLOOMBERG_ORANGE};
                color: white;
            }}
            
            /* Override default link styles for pills */
            .pill:not(.selected) {{
                color: {BLOOMBERG_TEXT} !important;
            }}

        

            
        </style>
        """,
        unsafe_allow_html=True
    )

def create_menu_html(selected_option, options):

    menu_html = '<div class="menu-container">'
    for option in options:
        active_class = "active" if option == selected_option else ""
        menu_html += (
            f'<a href="?menu={option}" class="menu-item {active_class}" '
            'target="_self">'
            f'{option}</a>'
        )
    menu_html += '</div>'
    return menu_html


def create_submenu_pills_html(selected_option, selected_sub, suboptions):

    pills_html = '<div class="pill-container">'
    for label in suboptions:
        is_selected = (label == selected_sub)
        selected_class = "selected" if is_selected else ""
        # URL = ?menu=<selected_option>&sub=<label>
        link = f'?menu={selected_option}&sub={label}'
        pill_html = (
            f'<a href="{link}" class="pill {selected_class}" target="_self">'
            f'{label}'
            f'</a>'
        )
        pills_html += pill_html
    pills_html += '</div>'
    return pills_html


def extract_fields_list(section_name, section_fields, config):

    fields_list = []
    default_vals = config["default_values"]
    units = config.get("variable_units", {})

    if isinstance(section_fields, dict) and "sub_category" in section_fields:
        sub_cat = section_fields["sub_category"]
        for sub_name, sub_conf in sub_cat.items():
            if "choices" in sub_conf:

                default_index = 0
                label = sub_name  
                key = f"{section_name}_{sub_name}"
                fields_list.append({
                    "type": "selectbox",
                    "label": label,
                    "options": sub_conf["choices"],
                    "default_index": default_index,
                    "key": key
                })

    elif isinstance(section_fields, list):
        for field in section_fields:
            label = field
            if field in units:
                label += f" ({units[field]})"
            default_value = float(default_vals.get(field, 0))
            step_val = 0.1 if "%" in label else 1.0
            key = f"{section_name}_{field}"
            fields_list.append({
                "type": "number_input",
                "label": label,
                "default": default_value,
                "step": step_val,
                "key": key
            })

    elif isinstance(section_fields, dict):
        for fname, finfo in section_fields.items():
            if isinstance(finfo, dict) and "choices" in finfo:

                choices = finfo["choices"]
                default_value = default_vals.get(fname, choices[0])
                default_index = choices.index(default_value) if default_value in choices else 0
                fields_list.append({
                    "type": "selectbox",
                    "label": fname,
                    "options": choices,
                    "default_index": default_index,
                    "key": f"{section_name}_{fname}"
                })
            else:

                default_val = default_vals.get(fname, 0)
                if isinstance(default_val, str):  
                    default_val = 0  
                else:
                    default_val = float(default_val)

                label = fname
                key = f"{section_name}_{fname}"
                fields_list.append({
                    "type": "number_input",
                    "label": label,
                    "default": default_val,
                    "step": 1.0,
                    "key": key
                })


    return fields_list


def render_input_sections_in_table(config):
    user_input = {}

    st.markdown("""
    <style>
    /* Supprime l'espacement par défaut en haut de la page */
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Table principale plus compacte */
    .input-table {
        width: 65%;
        margin: 0 auto;
        padding: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: stretch;
        border: none !important;
    }

    /* Lignes de la table */
    .section-row {
        display: flex;
        align-items: center;
        width: 100%;
        justify-content: space-between;
        padding: 0;
        margin: 0;
        border: none !important;
    }

    /* Colonne titre de section avec alignement vertical */
    .section-title-cell {
        display: flex;
        align-items: center;
        justify-content: center; 
        font-family: 'Bloomberg';
        color: white;
        font-size: 17px; /* Changez ici de 14px à 20px */
        font-weight: bold; /* Déjà en gras */
        min-width: 90px;
        max-width: 90px;
        text-align: center;
        padding: 0;
        margin: 0;
        border: none !important;
        height: 100%;
        min-height: 40px;
        flex-grow: 1;
        


    }




    
    /* ---- Inputs ---- */
    input, .stSelectbox select {{
        background-color: #333 !important;
        color: white !important;
        border: 1px solid {BLOOMBERG_ORANGE} !important;
    }}
    /* Dans la section CSS de apply_custom_styles() */
    /* Ajouter ceci */
    .stSelectbox [data-testid="stMarkdownContainer"] p {{
        color: white !important;
    }}
    /* Ajouter dans apply_custom_styles() */
    div[role="listbox"] ul li[aria-selected="true"] {{
        background-color: #E07D10 !important;
        color: black !important;
    }}
                
    /* Taille du selectbox (bouton principal) */
    .stSelectbox div[data-testid="stMarkdownContainer"] {{
        font-size: 16px !important;  /* Taille du texte */
        width: 200px !important;  /* Largeur */
        height: 50px !important;  /* Hauteur */
    }}
                








    </style>
    """, unsafe_allow_html=True)

    container = st.container()
    
    container.markdown('<div class="input-table">', unsafe_allow_html=True)

    # Boucle sur les sections
    for section_name, section_fields in config["variables"].items():
        fields_to_render = extract_fields_list(section_name, section_fields, config)

        # grouper par 4
        def chunker(seq, size=4):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        # 4 par ligne
        for idx, chunk in enumerate(chunker(fields_to_render, 4)):
            container.markdown('<div class="section-row">', unsafe_allow_html=True)
            
            cols = container.columns(5) 

            # Colonne 0 : titre de section
            with cols[0]:
                if idx == 0:
                    st.markdown(
                        f"""
                        <style>
                        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
                        
                        .section-title-cell {{
                            font-family: 'Oswald', sans-serif; /* Remplace par une des 5 propositions */
                            font-size: 18px; /* Ajuste la taille selon ton besoin */
                            font-weight: bold;
                        }}
                        </style>
                        <div class='section-title-cell'>{section_name}</div>
                        """,
                        unsafe_allow_html=True
                    )


                else:
                    st.markdown("<div class='section-title-cell'></div>", unsafe_allow_html=True)

            # Colonne 1 à 4 : inputs
            for i, field_def in enumerate(chunk):
                with cols[i + 1]:
                    if field_def["type"] == "selectbox":
                        user_val = st.selectbox(
                            label=field_def["label"],
                            options=field_def["options"],
                            index=field_def["default_index"],
                            key=field_def["key"]
                        )
                        user_input[field_def["label"]] = user_val
                    elif field_def["type"] == "number_input":
                        user_val = st.number_input(
                            label=field_def["label"],
                            value=field_def["default"],
                            step=field_def["step"],
                            key=field_def["key"]
                        )
                        user_input[field_def["label"]] = user_val
            
            container.markdown('</div>', unsafe_allow_html=True)

    container.markdown("</div>", unsafe_allow_html=True)

    return user_input


def display_greeks_table(greeks_dict):


    rounded_greeks = {key: f"{value:.2f}" for key, value in greeks_dict.items()}


    df = pd.DataFrame([rounded_greeks])


    df.columns = list(rounded_greeks.keys())


    df.index = ["Valeurs"]


    st.markdown("<h3>Les grecs de l'option sont :</h3>", unsafe_allow_html=True)
    st.dataframe(df)


def display_price_and_greeks_table(price, greeks):

    BLOOMBERG_YELLOW = "#FFB400"


    st.markdown(f"""
    <style>
    .pg-container {{
        display: flex;
        align-items: center; /* Centre verticalement */
        justify-content: center;
        gap: 20px;
        width: 100%;
    }}

    .pg-header {{
        color: {BLOOMBERG_YELLOW};
        font-size: 30px;
        font-weight: normal;  /* Pas en gras */
    }}

    .pg-value {{
        font-size: 24px;
        color: white;
        font-weight: bold;  /* En gras */
    }}

    .greeks-table-container {{
        display: flex;
        align-items: center; /* Centre verticalement */
        justify-content: center;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)


    if isinstance(greeks, dict):
        greeks = pd.DataFrame(greeks, index=["Value"])


    greeks = greeks.round(2)


    greeks_transposed = greeks.T


    st.markdown('<div class="pg-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        st.markdown('<div class="pg-header">Price :</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="pg-value">{price:.2f}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="pg-header">Greeks :</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="greeks-table-container">', unsafe_allow_html=True)
        st.dataframe(greeks_transposed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  


def display_price_and_prob_autocall(price, tab1, tab2):


    BLOOMBERG_YELLOW = "#FFB400"


    st.markdown(f"""
    <style>
    .pg-container {{
        display: flex;
        align-items: center; /* Centre verticalement */
        justify-content: center;
        gap: 20px;
        width: 100%;
    }}

    .pg-header {{
        color: {BLOOMBERG_YELLOW};
        font-size: 30px;
        font-weight: normal;  /* Pas en gras */
    }}

    .pg-value {{
        font-size: 24px;
        color: white;
        font-weight: bold;  /* En gras */
    }}

    .table-container {{
        display: flex;
        align-items: center; /* Centre verticalement */
        justify-content: center;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)


    if isinstance(tab1, dict):
        tab1 = pd.DataFrame(tab1, index=["Value"])
    
    if isinstance(tab2, dict):
        tab2 = pd.DataFrame(tab2, index=["Value"])


    tab1 = tab1.round(2)
    tab2 = tab2.round(2)


    tab1_transposed = tab1
    tab2_transposed = tab2.T


    st.markdown('<div class="pg-container">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1,1 , 5, 1, 3])

    with col1:
        st.markdown('<div class="pg-header">Price :</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="pg-value">{price:.2f}</div>', unsafe_allow_html=True)


    with col4:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(tab1_transposed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    

    with col6:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(tab2_transposed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  


def plot_option_graphs(option_instance, config):

    graph_mapping = {
        "Premium": "graph_price",
        "Payoff":  "graph_payoff",
        "Delta":   "graph_delta",
        "Gamma":   "graph_gamma",
        "Vega":    "graph_vega",
        "Theta":   "graph_theta",
        "Rho":     "graph_rho"
    }

    generated_graphs = {}

    greek_function = config.get("greek_function", None)
    payoff_function = config.get("payoff_function", None)
    pricing_function = config.get("pricing_function", None)


    if config.get("class") == BarrierOption:

        exercise_type = option_instance.type_exercise

        print(exercise_type)

        sub_dict = config["graph_variables"][exercise_type]  

        new_config = config.copy()
        new_config.update(sub_dict)

        config = new_config 


    if config.get("class") == LookbackOption:
  
        strike_type = option_instance.strike_type

        sub_dict = config["graph_variables"][strike_type] 


        new_config = config.copy()
        new_config.update(sub_dict)
        config = new_config

    if greek_function:
        greek_extractors = {
            "Delta": lambda opt, *a, **kw: greek_function(opt, *a, **kw)["Delta"],
            "Gamma": lambda opt, *a, **kw: greek_function(opt, *a, **kw)["Gamma"],
            "Vega":  lambda opt, *a, **kw: greek_function(opt, *a, **kw)["Vega"],
            "Theta": lambda opt, *a, **kw: greek_function(opt, *a, **kw)["Theta"],
            "Rho":   lambda opt, *a, **kw: greek_function(opt, *a, **kw)["Rho"]
        }



    else:
        greek_extractors = {}


    for title, key in graph_mapping.items():

        if key in config:

            graph_config = config[key]  
            plot_function = graph_config.get("function", None)
            extra_params = graph_config.get("add_parameters", {})
            
            if plot_function is None:
                continue

            if plot_function == Plotter:
                plotter = plot_function(option_instance,
                                        greek_method=greek_function,
                                        payoff_method=payoff_function,
                                        price_method=pricing_function,
                                        **extra_params)
                
                if title == "Premium":
                    fig = plotter.premium()
                elif title == "Payoff":
                    fig = plotter.payoff()
                elif title == "Delta":
                    fig = plotter.delta()
                elif title == "Gamma":
                    fig = plotter.gamma()
                elif title == "Vega":
                    fig = plotter.vega()
                elif title == "Theta":
                    fig = plotter.theta()
                elif title == "Rho":
                    fig = plotter.rho()
                else:
                    fig = None

                if fig:
                    generated_graphs[title] = fig

            elif plot_function == SmoothedGreek.interpolation:

                if title in greek_extractors:
                    greek_extractor = greek_extractors[title]
                    fig = plot_function(option_instance, greek_extractor, **extra_params)
                    generated_graphs[title] = fig

            elif plot_function == GreekPlotter.plot_strategy_greek:

                if title in ["Delta", "Gamma", "Vega", "Theta", "Rho"]:
                    fig = GreekPlotter.plot_strategy_greek(option_instance, title, **extra_params)
                    generated_graphs[title] = fig


            elif plot_function == OptionGraph.plot_strategy_price or plot_function == OptionGraph.plot_strategy_payoff:

                if title == "Premium":
                    fig = OptionGraph.plot_strategy_price(option_instance, **extra_params)
                    generated_graphs[title] = fig
                
                elif title == "Payoff":

                    fig = OptionGraph.plot_strategy_payoff(option_instance, **extra_params)
                    generated_graphs[title] = fig
            

            else:
                continue

    return generated_graphs




def plot_option_graphs2(option_instance, config):
    
    generated_graphs = {}
    

    graph_config = config.get("graph_price", {})
    plot_function = graph_config.get("function", None)
    extra_params = graph_config.get("add_parameters", {})
    
    if plot_function and plot_function == SmoothedGreek.interpolation:
        try:

            fig = plot_function(
                option_instance,
                lambda opt: opt.price(),  
                **extra_params
            )
            generated_graphs["Premium"] = fig
            
        except Exception as e:
            st.error(f"Erreur génération graphique Autocall : {str(e)}")

    return generated_graphs






def main():
    apply_custom_styles()


    menu_options = ["Vanilla Options", "Exotic Options", "Option Strategies", "Autocall"]


    suboptions_dict = {
        "Vanilla Options": ["European Option", "American Option"],
        "Exotic Options": [
            "Asian Option", "Barrier Option", "Digital Option",
            "Lookback Option", "Quanto Option"
        ],
        "Option Strategies": [
            "Call Spread", "Put Spread", "Butterfly Spread", "Condor Spread",
            "Straddle", "Strangle", "Risk Reversal"
        ],
        "Autocall": ["Athena", "Phoenix"]
    }


    query_params = st.query_params


    if "menu" in query_params and query_params["menu"]:
        selected_option = query_params["menu"]
        if selected_option not in menu_options:
            selected_option = menu_options[0]
    else:
        selected_option = menu_options[0]



    selected_sub = query_params.get("sub", "")

    sub_key = (selected_option, selected_sub)

    # Titre principal
    st.markdown('<div class="title">Greeks and Price</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="color: #0E1117; text-align: center; font-size: 15px; margin-top: -10px; margin-bottom: 0px;">'
        'ATTENTION: please click on the "..." in the top right corner, and switch to Dark Mode in stettings to properly visualize the application.</div>',
        unsafe_allow_html=True
    )

    
    #st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Menu principal
    st.markdown(create_menu_html(selected_option, menu_options), unsafe_allow_html=True)
    st.markdown('<div class="menu-separator"></div>', unsafe_allow_html=True)


    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    if selected_option in suboptions_dict:
        pills_html = create_submenu_pills_html(
            selected_option,
            selected_sub,
            suboptions_dict[selected_option]
        )
        st.markdown(pills_html, unsafe_allow_html=True)

    #st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
    
    if sub_key in option_data:
        config = option_data[sub_key]

        col1, col2, col3 = st.columns([1, 5, 1])  

        with col2:
            st.markdown(f'<hr style="border: 1px solid {BLOOMBERG_ORANGE};">', unsafe_allow_html=True)
            user_input = render_input_sections_in_table(config)
            st.markdown(f'<hr style="border: 1px solid {BLOOMBERG_ORANGE};">', unsafe_allow_html=True)


        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


        st.markdown('''
            <style>
            /* Import d'une police type Helvetica  */
            @import url('https://fonts.googleapis.com/css2?family=Helvetica:wght@700&display=swap');

            /* Sélection du "container" du bouton et centrage */
            .button-container {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                margin-top: 5px;
                margin-bottom: 20px;
            }

            /* Sélection du bouton généré par Streamlit */
            [data-testid="stButton"] {
                display: flex;
                justify-content: center;
                width: 100%;
            }

            [data-testid="stButton"] > button {
                background-color: #D32F2F !important; /* Rouge constant */
                color: black !important;             /* Texte en noir */
                font-size: 70px !important;          /* 2 fois plus grand (ex: 24 -> 48) */
                font-weight: 900 !important;         /* Texte en très gras */
                font-family: 'Helvetica', sans-serif !important;
                padding: 20px 60px !important;       /* Plus de padding pour un bouton plus imposant */
                border: none !important;
                border-radius: 8px !important;
                cursor: pointer !important;
                transition: background-color 0.3s ease !important;
                text-align: center !important;
                display: inline-block !important;
                margin: 0 auto !important;
            }

            /* Survol du bouton : un rouge plus foncé */
            [data-testid="stButton"] > button:hover {
                background-color: #B71C1C !important;
            }

            /* Optionnel : style de la zone résultat (si besoin) */
            .result-container {
                background-color: #3A3A3A;
                border: 2px solid #E07D10;
                border-radius: 8px;
                padding: 15px;
                margin-top: 25px;
                width: 80%;
                margin-left: auto;
                margin-right: auto;
                text-align: center;
            }

            .price-value {
                font-size: 50px;
                font-weight: bold;
                color: #FFD700;
                margin: 40px 0;
            }
            </style>
        ''', unsafe_allow_html=True)
    

        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:

            calculate_button = st.button("PRICE", key="calculate_button", use_container_width=True)


        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

        st.markdown(f'<hr style="border: 1px solid {BORDER_COLOR2}; width: 80%; margin: auto;">', unsafe_allow_html=True)


        #st.markdown("---")
        
        if calculate_button:

            pricing_params = {}
            for input_name, input_value in user_input.items():
                # Retirer l'unité du nom si présente (ex: "Volatility (%)" -> "Volatility")
                cleaned_name = input_name.split(" (")[0]
                
                variable_mapping = config.get("variable_mapping", {})
                param_name = variable_mapping.get(cleaned_name, cleaned_name)
                
                # Convertir les pourcentages en décimaux si nécessaire
                if (cleaned_name in config.get("variable_units", {}) 
                    and config["variable_units"][cleaned_name] == "%"):
                    input_value = input_value / 100.0
                

                if isinstance(input_value, str):
                    input_value = input_value.lower()

                pricing_params[param_name] = input_value

                if "strategy_type" in config:
                    pricing_params["strategy_type"] = config["strategy_type"]

            if config.get("class") == AutoCallOption and config.get("type_autocall") == "phoenix":
                pricing_params["type_autocall"] = "phoenix"

            elif config.get("class") == AutoCallOption and config.get("type_autocall") == "athena":
                pricing_params["barrier_coupon"] = pricing_params.get("barrier_early", None)  
                pricing_params["type_autocall"] = "athena"

            elif config.get("class") == VanillaOption and config.get("type_option") == "american":
                pricing_params["type_option"] = "american"
            
            # Appel à la fonction de pricing
            try:

                option_class = config["class"]
                option_instance = option_class(**pricing_params)
                

                price = config["pricing_function"](option_instance)
                


                # Appel à la fonction de calcul des grecs ou de proba pour les Autocall
                if config.get("class") == AutoCallOption:
                    tab1, tab2 = config["greek_function"](option_instance)

                    display_price_and_prob_autocall(price, tab1, tab2)

                else:
                    greeks = config["greek_function"](option_instance)

        

                    display_price_and_greeks_table(price, greeks)


                # Générer tous les graphiques liés à l'option
                if "option_graphs" not in st.session_state: 
                    st.session_state.option_graphs = {}

                if calculate_button:
                    if config.get("class") == AutoCallOption:
                        st.session_state.option_graphs = plot_option_graphs2(option_instance, config)
                    else:
                        st.session_state.option_graphs = plot_option_graphs(option_instance, config)



                if "option_graphs" in st.session_state and st.session_state.option_graphs:
                    option_graphs = st.session_state.option_graphs
                    available_graphs = list(option_graphs.keys())

                    # Création du bandeau avec onglets de graph
                    tabs = st.tabs(available_graphs)

                    # Afficher le graphique correspondant à l'onglet sélectionné
                    for tab, title in zip(tabs, available_graphs):
                        with tab:
                            #st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
                            st.plotly_chart(option_graphs[title], use_container_width=True)
                else:
                    st.warning("Aucun graphique disponible pour cette option.")



                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur lors du calcul: {str(e)}")
                st.error("Vérifiez vos paramètres d'entrée.")

    else:
        st.write("")





if __name__ == "__main__":
    main()
