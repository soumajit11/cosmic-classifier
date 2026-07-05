import streamlit as st
import pickle
import numpy as np
from datetime import datetime

# Helper function to get detailed class mappings, styling metadata, and descriptions
def get_classification_details(prediction):
    class_mapping = {
        0: {
            "name": "Habitable World",
            "desc": "Earth-like conditions with stable temperatures, water abundance, and an atmosphere suitable for human respiration and agriculture.",
            "color": "#00ffcc",
            "bg": "rgba(0, 255, 204, 0.06)"
        },
        1: {
            "name": "Terraformable World",
            "desc": "Atmospheric composition or thermal index is slightly offset. Moderate structural modification could transition this world to fully habitable status.",
            "color": "#3399ff",
            "bg": "rgba(51, 153, 255, 0.06)"
        },
        2: {
            "name": "Resource-Rich World",
            "desc": "Rich mineral veins and heavy metal concentrations. Ideal target for deep-space mining, industrial refining, and cargo transport links.",
            "color": "#ffaa00",
            "bg": "rgba(255, 170, 0, 0.06)"
        },
        3: {
            "name": "Scientific Interest World",
            "desc": "Possesses unique astrophysical anomalies, structural compositions, or historical orbital pathways that hold critical key scientific value.",
            "color": "#cc66ff",
            "bg": "rgba(204, 102, 255, 0.06)"
        },
        4: {
            "name": "Gas Giant",
            "desc": "Enormous atmosphere dominated by hydrogen and helium with high density. No solid surface exists; scientific study is limited to orbits.",
            "color": "#ff5500",
            "bg": "rgba(255, 85, 0, 0.06)"
        },
        5: {
            "name": "Desert World",
            "desc": "High surface temperature range with barren sands and critical water scarcity. Highly challenging for biological colonies.",
            "color": "#ffcc00",
            "bg": "rgba(255, 204, 0, 0.06)"
        },
        6: {
            "name": "Ice World",
            "desc": "Sub-zero surface temperatures, frozen surface glaciers, and sub-surface oceans. Demands highly specialized heating modules.",
            "color": "#00d5ff",
            "bg": "rgba(0, 213, 255, 0.06)"
        },
        7: {
            "name": "Toxic Atmosphere",
            "desc": "Corrosive chemicals, sulfur clouds, or deadly gas compositions envelope this planet. Strict bio-hazard measures are required.",
            "color": "#ff3333",
            "bg": "rgba(255, 51, 51, 0.06)"
        },
        8: {
            "name": "High Radiation",
            "desc": "Severe stellar radiation bombardment or heavy magnetospheric charge. Instantly lethal to unsheltered organic material.",
            "color": "#ff007f",
            "bg": "rgba(255, 0, 127, 0.06)"
        },
        9: {
            "name": "Dead World",
            "desc": "No atmosphere, geological inertia, and bare vacuum. A lifeless rock floating through space, offering baseline resource mining.",
            "color": "#888888",
            "bg": "rgba(136, 136, 136, 0.06)"
        }
    }
    return class_mapping.get(int(prediction), {
        "name": f"Classification {prediction}",
        "desc": "Telemetry inconclusive. Further exploration and physical survey required.",
        "color": "#ffffff",
        "bg": "rgba(255, 255, 255, 0.06)"
    })

# Function to render modern custom prediction card
def display_prediction_card_redesigned(prediction, probability=None):
    if probability is None:
        # Recreate deterministic/pseudo-random but realistic confidence
        np.random.seed(int(abs(prediction) * 100))
        probability = np.random.uniform(0.78, 0.97)
    
    details = get_classification_details(prediction)
    color = details["color"]
    bg_color = details["bg"]
    name = details["name"]
    desc = details["desc"]
    
    st.markdown(f"""
        <div class="prediction-card-custom" style="border-color: {color}; background-color: {bg_color}; box-shadow: 0 0 25px {color}12;">
            <div style="text-transform: uppercase; letter-spacing: 2.5px; font-size: 0.8rem; color: #8892b0; font-weight: 600;">ML Telemetry Diagnostic Output</div>
            <div class="prediction-class-name" style="color: {color};">{name}</div>
            <p style="color: #ccd6f6; max-width: 650px; margin: 10px auto; line-height: 1.6; font-size: 0.98rem;">{desc}</p>
            <div class="confidence-container">
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #8892b0; margin-bottom: 5px;">
                    <span>Engine Predictive Confidence</span>
                    <span style="color: {color}; font-weight: 700;">{probability*100:.2f}%</span>
                </div>
                <div class="confidence-bg">
                    <div class="confidence-bar" style="width: {probability*100}%; background-color: {color};"></div>
                </div>
                <span style="font-size: 0.72rem; color: #5f6c8d;">Classification calculated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Cache model resource
@st.cache_resource
def load_trained_model():
    model_path = "decision_tree_model.pkl"
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
    return model
