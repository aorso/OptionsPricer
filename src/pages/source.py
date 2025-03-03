
# sources.py

import streamlit as st
import os
import base64

# Définition des constantes de couleur identiques au profile
BLOOMBERG_BG = "#000000"
BLOOMBERG_ORANGE = "#E07D10"
BLOOMBERG_TEXT = "#FFFFFF"
BORDER_COLOR = "#808080"

def apply_custom_styles():

    st.markdown(
        f"""
        <style>
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
            .section-header {{
                font-size: 24px;
                color: {BLOOMBERG_ORANGE};
                margin: 25px 0 15px 0;
            }}
            hr {{
                border-top: 1px solid {BORDER_COLOR};
                margin: 30px 0;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():

    apply_custom_styles()

    # Titre principal
    st.markdown('<div class="title">Option Pricing Tool</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    

    # Contenu centré
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:

        st.markdown(
        f'<div class="source-link">All the code for option pricing and Greek calculations can be found '
        f'<a href="https://github.com/aorso/OptionsPricer/tree/main/src" target="_blank">here</a>.</div>',
        unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='line-height: 1.6;'>
        In this code, we implement three main approaches for pricing:
        
        <div style='margin: 20px 0 20px 20px;'>
        1. <span style='color:{0};'>Black–Scholes–Merton Model</span><br>
           <div style='padding-left: 25px;'>
           • Solutions for European vanilla options, Digital options, Quanto options, and Strategy combinations<br>
           • Fast and efficient for standard European-style derivatives
           </div>
        </div>
        
        <div style='margin: 20px 0 20px 20px;'>
        2. <span style='color:{0};'>Binomial Tree Method (Cox–Ross–Rubinstein)</span><br>
           <div style='padding-left: 25px;'>
           • Handles early exercise features of American options<br>
           • Accurately prices barrier options with discrete monitoring<br>
           • Visualizes option value evolution through time
           </div>
        </div>
        
        <div style='margin: 20px 0 20px 20px;'>
        3. <span style='color:{0};'>Monte Carlo Simulation (Geometric Brownian Motion)</span><br>
           <div style='padding-left: 25px;'>
           • Prices path-dependent options including Asian options, Lookback options, and Autocallables<br>
           • Calculates Greeks through numerical differentiation

           </div>
        </div>
        </div>
    """.format(BLOOMBERG_ORANGE), unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Section Modèle
        st.markdown('<div class="section-header">Model Assumptions</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='line-height: 1.6; margin-bottom: 30px;'>
        The tool operates under the assumptions of <span style='color:{BLOOMBERG_ORANGE};'>constant volatility</span>, 
        <span style='color:{BLOOMBERG_ORANGE};'>constant risk-free rate</span>, and 
        <span style='color:{BLOOMBERG_ORANGE};'>no-arbitrage conditions</span>. 
        While effective, this implementation represents a simplified model that excludes transaction costs and stochastic volatility.
        </div>
        """.format(BLOOMBERG_ORANGE=BLOOMBERG_ORANGE), unsafe_allow_html=True)


        st.markdown("<hr>", unsafe_allow_html=True)

        # Section Futures
        st.markdown('<div class="section-header">Future Enhancements</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='line-height: 1.6;'>
        Future enhancements will incorporate <span style='color:{BLOOMBERG_ORANGE};'>more realistic assumptions</span> such as:
        
        <div style='margin: 15px 0 15px 20px;'>
        • Jump diffusion models<br>
        • Term structure of volatility<br>
        • Yield curve modeling
        </div>

        This pricing tool is designed to evolve over time with planned additions including an educational section 
        explaining the underlying models and expanded functionality to price more specialized derivative products.
        </div>
        """.format(BLOOMBERG_ORANGE=BLOOMBERG_ORANGE), unsafe_allow_html=True)

if __name__ == "__main__":
    main()