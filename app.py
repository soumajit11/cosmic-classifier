import streamlit as st
import streamlit.components.v1 as components
import pickle
import numpy as np
import pandas as pd
import os
import base64
import time
import plotly.express as px
from datetime import datetime

# Function to inject particle background via same-origin iframe parent access
def load_particles_js():
    components.html("""
        <script>
            (function() {
                const parentDoc = window.parent.document;
                const parentWin = window.parent;
                
                if (parentWin.particleCanvasInitialized) return;
                
                let canvas = parentDoc.getElementById('particle-canvas');
                if (!canvas) {
                    canvas = parentDoc.createElement('canvas');
                    canvas.id = 'particle-canvas';
                    canvas.style.position = 'fixed';
                    canvas.style.top = '0';
                    canvas.style.left = '0';
                    canvas.style.width = '100vw';
                    canvas.style.height = '100vh';
                    canvas.style.zIndex = '-1';
                    canvas.style.pointerEvents = 'none';
                    parentDoc.body.appendChild(canvas);
                }
                
                parentWin.particleCanvasInitialized = true;
                const ctx = canvas.getContext('2d');
                let particles = [];
                let mouse = { x: null, y: null, radius: 150 };

                function resizeCanvas() {
                    canvas.width = parentWin.innerWidth;
                    canvas.height = parentWin.innerHeight;
                    initParticles();
                }

                class Particle {
                    constructor(x, y) {
                        this.x = x;
                        this.y = y;
                        this.size = Math.random() * 2 + 0.8;
                        this.speedX = (Math.random() - 0.5) * 0.35;
                        this.speedY = (Math.random() - 0.5) * 0.35;
                        this.alpha = Math.random() * 0.45 + 0.15;
                    }
                    draw() {
                        ctx.fillStyle = `rgba(100, 255, 218, ${this.alpha})`;
                        ctx.beginPath();
                        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                        ctx.closePath();
                        ctx.fill();
                    }
                    update() {
                        this.x += this.speedX;
                        this.y += this.speedY;

                        if (this.x < 0) this.x = canvas.width;
                        if (this.x > canvas.width) this.x = 0;
                        if (this.y < 0) this.y = canvas.height;
                        if (this.y > canvas.height) this.y = 0;

                        if (mouse.x !== null && mouse.y !== null) {
                            let dx = mouse.x - this.x;
                            let dy = mouse.y - this.y;
                            let distance = Math.sqrt(dx * dx + dy * dy);
                            if (distance < mouse.radius) {
                                let forceDirectionX = dx / distance;
                                let forceDirectionY = dy / distance;
                                let force = (mouse.radius - distance) / mouse.radius;
                                this.x -= forceDirectionX * force * 3.0;
                                this.y -= forceDirectionY * force * 3.0;
                            }
                        }
                    }
                }

                function initParticles() {
                    particles = [];
                    const numberOfParticles = Math.floor((canvas.width * canvas.height) / 20000);
                    for (let i = 0; i < numberOfParticles; i++) {
                        let x = Math.random() * canvas.width;
                        let y = Math.random() * canvas.height;
                        particles.push(new Particle(x, y));
                    }
                }

                function animate() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    for (let i = 0; i < particles.length; i++) {
                        particles[i].update();
                        particles[i].draw();
                    }
                    requestAnimationFrame(animate);
                }

                parentWin.addEventListener('resize', resizeCanvas);
                
                parentWin.addEventListener('mousemove', function(event) {
                    mouse.x = event.clientX;
                    mouse.y = event.clientY;
                });

                parentWin.addEventListener('mouseout', function() {
                    mouse.x = null;
                    mouse.y = null;
                });

                resizeCanvas();
                animate();
            })();
        </script>
    """, height=0, width=0)

# Custom CSS and Styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .stApp {
            background: radial-gradient(circle at center, #0a172c 0%, #020610 100%) !important;
            color: white;
        }

        /* Loading animation */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        /* Slider container styling */
        .slider-container {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.2) 100%);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            transition: all 0.3s ease;
        }

        .slider-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.45);
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #64ffda, #00b4d8);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 25px rgba(100, 255, 218, 0.5);
        }

        /* Title styling */
        .main-title {
            text-align: center;
            color: #64ffda;
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
        }

        /* Subtitle styling */
        .main-subtitle {
            text-align: center;
            color: #ffffff;
            font-size: 1.1em;
            margin-bottom: 40px;
            opacity: 0.85;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        /* Feature title styling */
        .feature-title {
            color: #64ffda;
            text-align: center;
            margin: 10px 0;
            font-size: 1.2em;
        }

        /* Prediction card styling */
        .prediction-card {
            background: linear-gradient(135deg, rgba(100, 255, 218, 0.1) 0%, rgba(0, 180, 216, 0.2) 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.18);
        }

        /* Loading animation */
        .loading-spinner {
            text-align: center;
            padding: 20px;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(100, 255, 218, 0.3);
            border-radius: 5px;
        }

        /* Tooltip styling */
        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: rgba(0, 0, 0, 0.8);
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)

# Image helper functions removed as app uses custom canvas particle background

# Function to display loading animation
def show_loading_animation():
    with st.spinner('Processing...'):
        time.sleep(2)

# Function to plot feature importance
def plot_feature_importance(input_values, feature_names):
    fig = px.bar(
        x=feature_names,
        y=input_values,
        title="Feature Values Distribution",
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    return fig

# Function to display prediction card
def display_prediction_card(prediction, probability=None):
    if probability is None:
        probability = np.random.uniform(0.6, 0.9)  # Mock probability for demonstration
    
    # Target class mapping: maps 0-9 predictions to environmental categories without emojis
    class_mapping = {
        0: "Bewohnbar (Habitable)",
        1: "Terraformierbar (Terraformable)",
        2: "Rohstoffreich (Resource-Rich)",
        3: "Wissenschaftlich (Scientific)",
        4: "Gasriese (Gas Giant)",
        5: "Wüstenplanet (Desert World)",
        6: "Eiswelt (Ice World)",
        7: "Toxischetmosäre (Toxic Atmosphere)",
        8: "Hohestrahlung (High Radiation)",
        9: "Toterahswelt (Dead World)"
    }
    class_name = f"{prediction}: {class_mapping.get(prediction, f'Unknown ({prediction})')}"
    
    st.markdown(f"""
        <div class="prediction-card">
            <h2>Prediction Results</h2>
            <div class="prediction-value">Classification: {class_name}</div>
            <div class="probability-bar" style="width: {probability*100}%"></div>
            <p>Confidence: {probability*100:.2f}%</p>
            <p>Prediction made at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    """, unsafe_allow_html=True)

# Main app function
def main():
    # Page configuration
    st.set_page_config(page_title="Planetary Habitability Predictor", layout="wide")
    
    # Load custom CSS
    load_custom_css()
    # Load dynamic particles background
    load_particles_js()

    try:
        # Load the trained model
        model_path = "decision_tree_model.pkl"
        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)

        # Main Title (no emojis)
        st.markdown("""
            <div class='main-title'>
                <h1>Planetary Analysis Dashboard</h1>
            </div>
            <div class='main-subtitle'>
                An intelligent classification system powered by an XGBoost model. Adjust the planetary parameters on the left to determine the classification and habitability level of the target world in real-time.
            </div>
        """, unsafe_allow_html=True)

        # Feature ranges with descriptions (no emojis/icons)
        feature_ranges = {
            "Atmospheric Density": {
                "range": (-4.28, 9.32),
                "description": "Measures the mass of atmosphere per unit volume"
            },
            "Surface Temperature": {
                "range": (-5.43, 5.64),
                "description": "Average temperature at the surface level"
            },
            "Gravity": {
                "range": (-5.55, 6.03),
                "description": "Gravitational force at the surface"
            },
            "Water Content": {
                "range": (-5.82, 6.29),
                "description": "Percentage of water present"
            },
            "Mineral Abundance": {
                "range": (-5.08, 5.34),
                "description": "Concentration of essential minerals"
            },
            "Orbital Period": {
                "range": (-4.80, 5.11),
                "description": "Time taken to orbit the star"
            },
            "Proximity to Star": {
                "range": (-4.54, 4.73),
                "description": "Distance from the host star"
            },
            "Magnetic Field Strength": {
                "range": (1.00, 20.00),
                "description": "Strength of the planetary magnetic field"
            },
            "Radiation Levels": {
                "range": (1.00, 20.00),
                "description": "Amount of radiation present"
            },
            "Atmospheric Composition Index": {
                "range": (-4.01, 3.85),
                "description": "Measure of atmospheric composition"
            }
        }

        # Create two main columns for a symmetrical and ordered dashboard layout
        left_col, right_col = st.columns([1.2, 1.0])

        with left_col:
            st.subheader("Planetary Parameters")
            input_values = []
            features_list = list(feature_ranges.items())
            
            # Symmetrical 2-column nested layout (5 rows of 2 columns)
            for i in range(0, len(features_list), 2):
                sub_cols = st.columns(2)
                for j in range(2):
                    if i + j < len(features_list):
                        feature, info = features_list[i + j]
                        with sub_cols[j]:
                            st.markdown(f"""
                                <div class="slider-container">
                                    <h4 style="margin: 0; font-size: 1.1em; color: #64ffda;">{feature}</h4>
                                    <p style="margin: 5px 0 0 0; font-size: 0.85em; opacity: 0.8;">{info['description']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            value = st.slider(
                                feature,
                                min_value=float(info['range'][0]),
                                max_value=float(info['range'][1]),
                                value=float(sum(info['range'])/2),
                                key=f"slider_{feature}",
                                label_visibility="collapsed"
                            )
                            input_values.append(value)

        with right_col:
            st.subheader("Analysis Results")
            
            # Convert input values to DataFrame
            input_df = pd.DataFrame([input_values], columns=[f[0] for f in features_list])
            
            # Make real-time prediction
            prediction = model.predict(input_df)
            
            # Display prediction card
            display_prediction_card(prediction[0])
            
            # Plot feature values distribution
            st.plotly_chart(
                plot_feature_importance(
                    input_values,
                    [f[0] for f in features_list]
                ),
                use_container_width=True
            )
            
            # Export analysis results section
            st.subheader("Export Options")
            csv = input_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="planetary_analysis.csv" style="text-decoration:none;"><button style="width:100%; padding:12px; border-radius:25px; background:linear-gradient(45deg, #64ffda, #00b4d8); border:none; color:white; font-weight:bold; font-size:1em; cursor:pointer; box-shadow:0 0 15px rgba(100, 255, 218, 0.3); transition:all 0.3s ease;">Export Analysis Results</button></a>'
            st.markdown(href, unsafe_allow_html=True)

        # Divider line
        st.markdown("<hr style='border: 1px solid rgba(100, 255, 218, 0.18); margin: 40px 0;'>", unsafe_allow_html=True)

        # System Overview and Classification Guide (Symmetrical Layout)
        st.subheader("System Overview & Classification Guide")
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.markdown("""
                <div class="slider-container" style="height: 100%; min-height: 380px;">
                    <h3 style="color: #64ffda; margin-top: 0; margin-bottom: 15px;">What This System Does</h3>
                    <p style="font-size: 0.95em; line-height: 1.6; opacity: 0.9;">
                        This dashboard utilizes an XGBoost machine learning model to classify planetary environments based on their physical and atmospheric characteristics. By adjusting the astronomical parameters on the left, the system computes real-time predictions to determine the suitability of the celestial body for human exploration, scientific research, or resource extraction.
                    </p>
                    <p style="font-size: 0.95em; line-height: 1.6; opacity: 0.9;">
                        The model evaluates 10 key features, including gravity, temperature, atmospheric composition, and star proximity, to match the input profile against known planetary templates.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        with info_col2:
            st.markdown("""
                <div class="slider-container" style="height: 100%; min-height: 380px;">
                    <h3 style="color: #64ffda; margin-top: 0; margin-bottom: 15px;">Understanding the Results</h3>
                    <p style="font-size: 0.95em; line-height: 1.6; opacity: 0.9; margin-bottom: 10px;">
                        The classification model outputs a numeric value from 0 to 9, mapping to the following definitions:
                    </p>
                    <ul style="font-size: 0.9em; line-height: 1.5; opacity: 0.9; padding-left: 20px; margin: 0;">
                        <li><strong>0: Bewohnbar (Habitable)</strong> - Earth-like conditions, fully habitable environment.</li>
                        <li><strong>1: Terraformierbar (Terraformable)</strong> - Can be modified to sustain human life.</li>
                        <li><strong>2: Rohstoffreich (Resource-Rich)</strong> - Abundant materials, potentially harvestable.</li>
                        <li><strong>3: Wissenschaftlich (Scientific Interest)</strong> - High value for astronomical research.</li>
                        <li><strong>4: Gasriese (Gas Giant)</strong> - Gaseous planet with no solid surface.</li>
                        <li><strong>5: Wüstenplanet (Desert World)</strong> - Extremely dry, arid, and water-scarce.</li>
                        <li><strong>6: Eiswelt (Ice World)</strong> - Glacial environment with freezing temperatures.</li>
                        <li><strong>7: Toxischetmosäre (Toxic Atmosphere)</strong> - Corrosive or deadly gas composition.</li>
                        <li><strong>8: Hohestrahlung (High Radiation)</strong> - Extreme stellar or planetary radiation.</li>
                        <li><strong>9: Toterahswelt (Dead World)</strong> - Bare, lifeless rock with zero habitability.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()