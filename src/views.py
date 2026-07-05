import streamlit as st
import pandas as pd
import base64
import time
from src.charts import plot_feature_importance, plot_radar_chart
from src.model_utils import display_prediction_card_redesigned

# Render Landing Page
def render_landing_page():
    st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 15px;">
            <h1 class="main-title">COSMIC CLASSIFIER AI</h1>
            <p class="main-subtitle">An intelligent deep-space diagnostic platform. Calibrate parameters to determine habitability indexes and physical classifications of remote celestial bodies in real-time.</p>
        </div>
    """, unsafe_allow_html=True)

    # Full-width card describing Diagnostic Protocol
    st.markdown("""
        <div class="glass-card" style="margin-bottom: 25px; padding: 35px;">
            <h3 style="color: #64ffda; margin-top: 0; margin-bottom: 20px; text-align: center;">Diagnostic Protocol</h3>
            <p style="color: #a8b2d1; font-size: 1.02rem; line-height: 1.8; margin-bottom: 20px; text-align: center; max-width: 900px; margin-left: auto; margin-right: auto;">
                Welcome to the Planetary Telemetry Diagnostic Deck. The Cosmic Classifier AI leverages a trained machine learning model to evaluate atmospheric, physical, and stellar conditions, matching telemetry inputs to a specific environmental catalog.
            </p>
            <div style="max-width: 650px; margin: 0 auto; color: #a8b2d1; font-size: 0.98rem; line-height: 1.8;">
                <p style="font-weight: 600; color: #ccd6f6; margin-bottom: 10px; text-align: center;">Protocol Execution Guidelines:</p>
                <ol style="padding-left: 20px; margin-bottom: 0;">
                    <li>Configure planetary parameters across the three core scientific spheres.</li>
                    <li>Analyze custom radar telemetry signatures and numerical trends.</li>
                    <li>Export telemetry reports for interstellar navigation systems.</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color: #64ffda; text-align: center; margin-top: 30px; margin-bottom: 15px; font-size: 1.4rem;'>Telemetry Classifier Catalog</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="class-grid">
            <div class="class-badge" style="border-left: 3px solid #00ffcc;"><span style="color: #00ffcc; font-weight: 700;">0</span> Habitable World</div>
            <div class="class-badge" style="border-left: 3px solid #3399ff;"><span style="color: #3399ff; font-weight: 700;">1</span> Terraformable</div>
            <div class="class-badge" style="border-left: 3px solid #ffaa00;"><span style="color: #ffaa00; font-weight: 700;">2</span> Resource-Rich</div>
            <div class="class-badge" style="border-left: 3px solid #cc66ff;"><span style="color: #cc66ff; font-weight: 700;">3</span> Scientific Value</div>
            <div class="class-badge" style="border-left: 3px solid #ff5500;"><span style="color: #ff5500; font-weight: 700;">4</span> Gas Giant</div>
            <div class="class-badge" style="border-left: 3px solid #ffcc00;"><span style="color: #ffcc00; font-weight: 700;">5</span> Desert World</div>
            <div class="class-badge" style="border-left: 3px solid #00d5ff;"><span style="color: #00d5ff; font-weight: 700;">6</span> Ice World</div>
            <div class="class-badge" style="border-left: 3px solid #ff3333;"><span style="color: #ff3333; font-weight: 700;">7</span> Toxic Atmosphere</div>
            <div class="class-badge" style="border-left: 3px solid #ff007f;"><span style="color: #ff007f; font-weight: 700;">8</span> High Radiation</div>
            <div class="class-badge" style="border-left: 3px solid #888888;"><span style="color: #888888; font-weight: 700;">9</span> Dead World</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1.2, 1.2, 1.2])
    with col_center:
        if st.button("Access Telemetry Deck", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()

# Render Parameter Input Page
def render_input_page(feature_ranges):
    st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 25px;">
            <h2 style="color: #64ffda; font-size: 2.2rem; font-weight: 700; margin-bottom: 5px;">Planetary Parameter Telemetry</h2>
            <p style="color: #a8b2d1; font-size: 1rem; max-width: 650px; margin: 0 auto;">
                Calibrate the astrophysical metrics below. Features are grouped into distinct diagnostic spheres to prevent clutter.
            </p>
        </div>
    """, unsafe_allow_html=True)

    atmosphere_features = ["Atmospheric Density", "Surface Temperature", "Atmospheric Composition Index"]
    structure_features = ["Gravity", "Water Content", "Mineral Abundance"]
    orbital_features = ["Orbital Period", "Proximity to Star", "Magnetic Field Strength", "Radiation Levels"]

    tab1, tab2, tab3 = st.tabs([
        "Climate and Atmosphere", 
        "Planetary Structure", 
        "Stellar and Orbital Dynamics"
    ])

    with tab1:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for i, feature in enumerate(atmosphere_features):
            info = feature_ranges[feature]
            current_val = st.session_state.inputs[feature]
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.markdown(f"""
                    <div class="slider-container">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 style="margin: 0; font-size: 1rem; color: #64ffda; font-weight: 600;">{feature}</h4>
                            <span style="font-size:0.9rem; color:#64ffda; font-weight:700;">{current_val:.2f}</span>
                        </div>
                        <p style="margin: 4px 0 8px 0; font-size: 0.82rem; color: #8892b0; min-height: 25px; line-height: 1.4;">{info['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                val = st.slider(
                    feature,
                    min_value=float(info['range'][0]),
                    max_value=float(info['range'][1]),
                    value=current_val,
                    key=f"slider_{feature}",
                    label_visibility="collapsed"
                )
                st.session_state.inputs[feature] = val

    with tab2:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for i, feature in enumerate(structure_features):
            info = feature_ranges[feature]
            current_val = st.session_state.inputs[feature]
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.markdown(f"""
                    <div class="slider-container">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 style="margin: 0; font-size: 1rem; color: #64ffda; font-weight: 600;">{feature}</h4>
                            <span style="font-size:0.9rem; color:#64ffda; font-weight:700;">{current_val:.2f}</span>
                        </div>
                        <p style="margin: 4px 0 8px 0; font-size: 0.82rem; color: #8892b0; min-height: 25px; line-height: 1.4;">{info['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                val = st.slider(
                    feature,
                    min_value=float(info['range'][0]),
                    max_value=float(info['range'][1]),
                    value=current_val,
                    key=f"slider_{feature}",
                    label_visibility="collapsed"
                )
                st.session_state.inputs[feature] = val

    with tab3:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for i, feature in enumerate(orbital_features):
            info = feature_ranges[feature]
            current_val = st.session_state.inputs[feature]
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.markdown(f"""
                    <div class="slider-container">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 style="margin: 0; font-size: 1rem; color: #64ffda; font-weight: 600;">{feature}</h4>
                            <span style="font-size:0.9rem; color:#64ffda; font-weight:700;">{current_val:.2f}</span>
                        </div>
                        <p style="margin: 4px 0 8px 0; font-size: 0.82rem; color: #8892b0; min-height: 25px; line-height: 1.4;">{info['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                val = st.slider(
                    feature,
                    min_value=float(info['range'][0]),
                    max_value=float(info['range'][1]),
                    value=current_val,
                    key=f"slider_{feature}",
                    label_visibility="collapsed"
                )
                st.session_state.inputs[feature] = val

    st.markdown("<hr style='border: 1px solid rgba(100, 255, 218, 0.08); margin: 30px 0;'>", unsafe_allow_html=True)

    col_nav1, _, col_nav2 = st.columns([1.2, 2.5, 1.2])
    with col_nav1:
        if st.button("Return to Port", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    with col_nav2:
        if st.button("Run Cosmic Classification", use_container_width=True):
            with st.spinner('Calibrating telemetry systems and classification engines...'):
                time.sleep(1.2)
            st.session_state.page = "output"
            st.rerun()

# Render Output & Visualization Page
def render_output_page(model, feature_ranges):
    st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 25px;">
            <h2 style="color: #64ffda; font-size: 2.2rem; font-weight: 700; margin-bottom: 5px;">Diagnostic & Visualization Deck</h2>
            <p style="color: #a8b2d1; font-size: 1rem; max-width: 650px; margin: 0 auto;">
                Diagnostic scanning is complete. Review predicted results and interact with visual telemetry models.
            </p>
        </div>
    """, unsafe_allow_html=True)

    features_list = list(feature_ranges.keys())
    input_values = [st.session_state.inputs[f] for f in features_list]
    input_df = pd.DataFrame([input_values], columns=features_list)

    # Run Prediction
    prediction = model.predict(input_df)[0]

    # Show prediction card
    display_prediction_card_redesigned(prediction)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Visualizations Side-by-Side wrapped in border containers for unified styling
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("""
                <h4 style="color: #64ffda; margin-top: 0; margin-bottom: 5px; text-align: center; font-weight: 600;">Planetary Signature Radar</h4>
                <p style="font-size: 0.8rem; color: #8892b0; text-align: center; margin-bottom: 10px;">Normalized telemetry bounds mapped on a polar projection index.</p>
            """, unsafe_allow_html=True)
            radar_fig = plot_radar_chart(input_values, features_list, feature_ranges)
            st.plotly_chart(radar_fig, use_container_width=True)
        
    with col2:
        with st.container(border=True):
            st.markdown("""
                <h4 style="color: #64ffda; margin-top: 0; margin-bottom: 5px; text-align: center; font-weight: 600;">Numeric Metrics Spectrum</h4>
                <p style="font-size: 0.8rem; color: #8892b0; text-align: center; margin-bottom: 10px;">Raw quantitative telemetry values across all configured feature sliders.</p>
            """, unsafe_allow_html=True)
            bar_fig = plot_feature_importance(input_values, features_list)
            st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown("<hr style='border: 1px solid rgba(100, 255, 218, 0.08); margin: 30px 0;'>", unsafe_allow_html=True)

    # mirrord bottom navigation
    col_act1, _, col_act2, _, col_act3 = st.columns([1.2, 0.2, 1.4, 0.2, 1.2])
    with col_act1:
        if st.button("Adjust Parameters", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()
            
    with col_act2:
        csv = input_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="planetary_analysis.csv" style="text-decoration:none;"><button class="btn-primary" style="width:100%; padding:10px; border-radius:25px; border:none; font-weight:bold; font-size:0.95rem; cursor:pointer;">Export Diagnostics Data</button></a>'
        st.markdown(href, unsafe_allow_html=True)
        
    with col_act3:
        if st.button("Return to Port", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
