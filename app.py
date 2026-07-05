import streamlit as st
import pandas as pd
from src.styles import load_custom_css, load_parent_enhancements
from src.model_utils import load_trained_model
from src.views import render_landing_page, render_input_page, render_output_page

# Main app function
def main():
    # Page configuration
    st.set_page_config(page_title="Planetary Habitability Predictor", layout="wide")
    
    # Load custom CSS and parent modifications
    load_custom_css()
    load_parent_enhancements()

    try:
        # Load the trained model
        model = load_trained_model()

        # Telemetry Feature ranges & details
        feature_ranges = {
            "Atmospheric Density": {
                "range": (-4.28, 9.32),
                "description": "Measures the mass density of the atmosphere per unit volume."
            },
            "Surface Temperature": {
                "range": (-5.43, 5.64),
                "description": "Average planetary temperature measured at surface level."
            },
            "Gravity": {
                "range": (-5.55, 6.03),
                "description": "Gravitational pull acceleration value at the planetary crust."
            },
            "Water Content": {
                "range": (-5.82, 6.29),
                "description": "Total percentage value of surface water hydration abundance."
            },
            "Mineral Abundance": {
                "range": (-5.08, 5.34),
                "description": "Aggregate concentration of strategic minerals and resource compounds."
            },
            "Orbital Period": {
                "range": (-4.80, 5.11),
                "description": "Total local days required to complete a full orbital trajectory."
            },
            "Proximity to Star": {
                "range": (-4.54, 4.73),
                "description": "Mean distance of planetary orbit from the parent host star."
            },
            "Magnetic Field Strength": {
                "range": (1.00, 20.00),
                "description": "Strength index of the global planetary magnetic shield."
            },
            "Radiation Levels": {
                "range": (1.00, 20.00),
                "description": "Aggregated cosmic and local planetary surface radiation index."
            },
            "Atmospheric Composition Index": {
                "range": (-4.01, 3.85),
                "description": "Composite chemical signature value of gaseous atmospheric compounds."
            }
        }

        # Initialize session state for page
        if 'page' not in st.session_state:
            st.session_state.page = 'landing'
            
        # Initialize inputs in session state if not present
        if 'inputs' not in st.session_state:
            st.session_state.inputs = {}
            for feature, info in feature_ranges.items():
                st.session_state.inputs[feature] = float(sum(info['range']) / 2)

        # Render Clickable Interactive Step Indicator Navbar (completely emoji-free, bracket active design)
        _, nav_col, _ = st.columns([1, 4, 1])
        with nav_col:
            c1, c2, c3 = st.columns(3)
            with c1:
                lbl = "[ Welcome ]" if st.session_state.page == "landing" else "Welcome"
                if st.button(lbl, key="nav_btn_landing", use_container_width=True):
                    st.session_state.page = "landing"
                    st.rerun()
            with c2:
                lbl = "[ Configure Parameters ]" if st.session_state.page == "input" else "Configure Parameters"
                if st.button(lbl, key="nav_btn_input", use_container_width=True):
                    st.session_state.page = "input"
                    st.rerun()
            with c3:
                lbl = "[ Diagnostic Report ]" if st.session_state.page == "output" else "Diagnostic Report"
                if st.button(lbl, key="nav_btn_output", use_container_width=True):
                    st.session_state.page = "output"
                    st.rerun()

        # Multi-page router
        if st.session_state.page == "landing":
            render_landing_page()
        elif st.session_state.page == "input":
            render_input_page(feature_ranges)
        elif st.session_state.page == "output":
            render_output_page(model, feature_ranges)

    except Exception as e:
        st.error(f"A diagnostic system error occurred: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()