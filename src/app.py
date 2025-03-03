
# app.py

import streamlit as st
import importlib
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Option Pricer", layout="wide", page_icon="📈")


st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .css-1d391kg {padding-top: 1rem;} /* Ajustement du padding de la sidebar */
    </style>
""", unsafe_allow_html=True)


BLOOMBERG_BLUE = "#3A5AB4"
BLOOMBERG_GRAY = "#D9D9D9"
BACKGROUND_COLOR = "#1E1E1E"  

# Barre latérale avec les boutons
with st.sidebar:
    st.markdown(f'<style>.css-1d391kg {{background-color: {BACKGROUND_COLOR};}}</style>', unsafe_allow_html=True)

    selected_section = option_menu(
        menu_title=None,  
        options=["Pricer", "Source", "Profile"],  
        icons=["graph-up", "book",  "person"],  
        menu_icon=None, 
        default_index=0,  
        styles={
            "container": {
                "padding": "0!important",
                "background-color": BACKGROUND_COLOR,  
            },
            "icon": {
                "color": BLOOMBERG_GRAY,  
                "font-size": "18px",
            },
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "padding": "12px",
                "margin": "5px 0",
                "border-radius": "5px",
                "--hover-color": "#333333",  
            },
            "nav-link-selected": {
                "background-color": BLOOMBERG_BLUE,  
                "color": "white",
                "border-radius": "5px",
            },
        }
    )


pages = {
    "Pricer": "pages.pricer",
    "Source": "pages.source",
    "Profile": "pages.profile"
    
}

if selected_section in pages:
    module = importlib.import_module(pages[selected_section])
    module.main() 
