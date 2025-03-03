# Derivatives Pricer

**An interactive pricing tool for structured and exotic options, developed with Python and Streamlit.**  
This project provides a fast and intuitive interface for option pricing and risk analysis, supporting various pricing models and option types.  

---

## 📂 Supported Options  
- **Vanilla Options**:  Calls and Puts  (European/American)
- **Exotic Options**: Asian, Lookback, Quanto, Digits, Barrier Options (European/American)
- **Structured Products and Strategies**:  Autocall (Phenix,Athena), Condor Spread, Butterfly Spread, ...
- **Pricing Models**: Black-Scholes, Binomial Tree, Monte Carlo  
- **Greek Calculations**: Delta, Gamma, Vega, Theta, Rho  

---

## 🏗️ Project Structure  

📂 `models/` → **Pricing and Greek calculation modules**  
 ┣ 📂 `greek_method/` → Computes option Greeks (Binomial, Monte Carlo, Black-Scholes)  
 ┣ 📂 `option_models/` → Defines different option types (Vanilla, Asian, Lookback, Quanto, Barrier, Digits, etc.)  
 ┣ 📂 `plot_tools/` → Visualization tools for pricing and Greeks  
 ┗ 📂 `pricing_method/` → Implements pricing models (Monte Carlo, Black-Scholes, Binomial Tree)  

📂 `pages/` → **Streamlit interface components**  
 ┣ 📜 `pricer.py` → Main pricing interface  
 ┣ 📜 `profile.py` → User profile page  
 ┗ 📜 `source.py` → Documentation and methodology section  

📜 `app.py` → **Launches the Streamlit web app**  

---

## 📊 Features  
✅ Interactive selection of option parameters  
✅ Real-time pricing results  
✅ Visualization of risk metrics and payout scenarios  

---

## 🛠️ Technologies  
- **Python** 🐍  
- **Streamlit** (Interactive web UI)  
- **NumPy & Pandas** (Data manipulation)  
- **Plotly** (Graphical visualization)  
- **Scipy** (Scientific computing)  

---
