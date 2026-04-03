import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="ImpactSense - Earthquake Prediction",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main {
        background: transparent;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 40px 20px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 20px 0 40px 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #555;
        margin: 10px 0;
        font-weight: 300;
    }
    
    .hero-description {
        font-size: 1rem;
        color: #777;
        margin-top: 15px;
    }
    
    /* Input Card */
    .input-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.2);
        margin: 20px 0;
        animation: fadeIn 1s ease-in;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 30px;
        text-align: center;
        position: relative;
        padding-bottom: 15px;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Input Labels */
    .stNumberInput label, .stSlider label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #333 !important;
        margin-bottom: 10px !important;
    }
    
    /* Number Input Styling */
    .stNumberInput input {
        background: #f8f9fa !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Predict Button */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 20px 60px !important;
        border-radius: 50px !important;
        font-size: 1.3rem !important;
        letter-spacing: 1px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        text-transform: uppercase !important;
        width: 100% !important;
        margin-top: 30px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Alert Cards */
    .alert-card {
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: zoomIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 3px solid rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.5) rotate(-10deg);
        }
        to {
            opacity: 1;
            transform: scale(1) rotate(0deg);
        }
    }
    
    .alert-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .green-alert {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
    }
    
    .yellow-alert {
        background: linear-gradient(135deg, #f7b733 0%, #fc4a1a 100%);
        color: white;
    }
    
    .orange-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
    }
    
    .red-alert {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
    
    .alert-icon {
        font-size: 8rem;
        margin-bottom: 20px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    .alert-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 20px 0;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    
    .alert-confidence {
        font-size: 1.8rem;
        font-weight: 300;
        margin-top: 15px;
        opacity: 0.95;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #777;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Recommendation Box */
    .recommendation-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        border-left: 6px solid #667eea;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .recommendation-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 15px;
    }
    
    .recommendation-text {
        font-size: 1.1rem;
        color: #555;
        line-height: 1.8;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin-top: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .footer-text {
        color: #777;
        font-size: 0.9rem;
    }
    
    /* Pulse Animation for Icons */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .pulse-icon {
        animation: pulse 2s infinite;
    }
    </style>
""", unsafe_allow_html=True)

# Load model function
@st.cache_resource
def load_model():
    try:
        with open('earthquake_model.pkl', 'rb') as f:
            model_artifacts = pickle.load(f)
        return model_artifacts
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please ensure 'earthquake_model.pkl' is in the same directory.")
        return None

# Prediction function
def predict_earthquake(magnitude, depth, cdi, mmi, sig, model_artifacts):
    input_data = pd.DataFrame([[magnitude, depth, cdi, mmi, sig]], 
                              columns=['magnitude', 'depth', 'cdi', 'mmi', 'sig'])
    
    input_data['impact_score'] = input_data['magnitude'] * input_data['sig']
    input_data['depth_mag_ratio'] = input_data['depth'] / (input_data['magnitude'] + 1)
    
    scaler = model_artifacts['scaler']
    model = model_artifacts['model']
    label_encoder = model_artifacts['label_encoder']
    outlier_bounds = model_artifacts['outlier_bounds']
    feature_names = model_artifacts['feature_names']
    
    for col in feature_names:
        lower, upper = outlier_bounds[col]
        input_data[col] = np.clip(input_data[col], lower, upper)
    
    input_scaled = scaler.transform(input_data[feature_names])
    
    prediction_encoded = model.predict(input_scaled)[0]
    prediction_proba = model.predict_proba(input_scaled)[0]
    prediction = label_encoder.inverse_transform([prediction_encoded])[0]
    
    return prediction, prediction_proba, label_encoder.classes_

# Hero Section
st.markdown("""
    <div class='hero-section'>
        <div class='pulse-icon' style='font-size: 5rem;'>🌍</div>
        <h1 class='hero-title'>ImpactSense</h1>
        <p class='hero-subtitle'>Earthquake Impact Prediction System</p>
        <p class='hero-description'>
             Advanced earthquake alert prediction system for disaster management<br>
             Real-time seismic risk assessment for emergency preparedness
        </p>
    </div>
""", unsafe_allow_html=True)

# Load model
model_artifacts = load_model()

if model_artifacts:
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Model Status")
        st.markdown(f"""
        <div class='info-box'>
        <b>Algorithm:</b> {model_artifacts['model_name']}<br>
        <b>Accuracy:</b> <span style='color: #27ae60; font-weight: 700;'>{model_artifacts['accuracy']:.2f}%</span><br>
        <b>Status:</b> <span style='color: green;'>● Online</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚨 Alert Levels Guide")
        st.markdown("""
        <div style='padding: 15px; background: white; border-radius: 12px; margin: 10px 0;'>
        <div style='margin: 10px 0; padding: 10px; background: linear-gradient(135deg, #56ab2f, #a8e063); color: white; border-radius: 8px; font-weight: 600;'>
        🟢 GREEN: Minimal Impact
        </div>
        <div style='margin: 10px 0; padding: 10px; background: linear-gradient(135deg, #f7b733, #fc4a1a); color: white; border-radius: 8px; font-weight: 600;'>
        🟡 YELLOW: Low Impact
        </div>
        <div style='margin: 10px 0; padding: 10px; background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; border-radius: 8px; font-weight: 600;'>
        🟠 ORANGE: Moderate Impact
        </div>
        <div style='margin: 10px 0; padding: 10px; background: linear-gradient(135deg, #eb3349, #f45c43); color: white; border-radius: 8px; font-weight: 600;'>
        🔴 RED: High Impact
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Parameter Guide")
        st.markdown("""
        <div class='info-box'>
        <b>Magnitude:</b> Earthquake strength (0-9)<br>
        <b>Depth:</b> Distance below surface (0-1000 km)<br>
        <b>CDI:</b> Community felt intensity (0-10)<br>
        <b>MMI:</b> Instrumental intensity (0-10)<br>
        <b>Significance:</b> Overall impact score (-300-1000)
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 15px;'>
        <p style='color: #888; font-size: 0.85rem; margin: 0;'>
        Developed by Pooja Yadav
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Input Section
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>🎛️ Enter Earthquake Parameters</h2>", unsafe_allow_html=True)
    
    # Create columns for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div style='margin: 25px 0;'>", unsafe_allow_html=True)
        magnitude = st.number_input(
            "🌊 Magnitude",
            min_value=0.0,
            max_value=9.0,
            value=0.0,
            step=0.1,
            help="Earthquake magnitude on the Richter scale (0.0 - 9.0)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 25px 0;'>", unsafe_allow_html=True)
        depth = st.number_input(
            "📏 Depth (km)",
            min_value=0.0,
            max_value=1000.0,
            value=0.0,
            step=1.0,
            help="Depth of earthquake hypocenter in kilometers (0 - 1000)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 25px 0;'>", unsafe_allow_html=True)
        cdi = st.number_input(
            "📍 CDI (Community Decimal Intensity)",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.1,
            help="Felt intensity reported by community (0.0 - 10.0)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='margin: 25px 0;'>", unsafe_allow_html=True)
        mmi = st.number_input(
            "📊 MMI (Modified Mercalli Intensity)",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.1,
            help="Instrumental intensity measurement (0.0 - 10.0)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 25px 0;'>", unsafe_allow_html=True)
        sig = st.number_input(
            "⚡ Significance",
            min_value=-300,
            max_value=1000,
            value=0,
            step=10,
            help="Overall significance score (-300 - 1000)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Predict Button
    predict_button = st.button("🎯 PREDICT ALERT LEVEL", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prediction Results
    if predict_button:
        
        # Loading animation
        with st.spinner("🔄 Analyzing seismic parameters..."):
            time.sleep(1.5)  # Dramatic pause for effect
            prediction, proba, classes = predict_earthquake(
                magnitude, depth, cdi, mmi, sig, model_artifacts
            )
        
        # Alert configurations
        alert_config = {
            'green': {
                'class': 'green-alert',
                'icon': '🟢',
                'color': '#27ae60',
                'title': 'GREEN ALERT',
                'message': 'Minimal seismic impact detected. Continue normal operations with standard monitoring protocols.',
                'risk': 'LOW'
            },
            'yellow': {
                'class': 'yellow-alert',
                'icon': '🟡',
                'color': '#f39c12',
                'title': 'YELLOW ALERT',
                'message': 'Low to moderate impact expected. Stay alert and prepare emergency supplies. Review evacuation plans.',
                'risk': 'MODERATE'
            },
            'orange': {
                'class': 'orange-alert',
                'icon': '🟠',
                'color': '#e67e22',
                'title': 'ORANGE ALERT',
                'message': 'Significant impact anticipated! Activate emergency response teams. Evacuate vulnerable areas immediately.',
                'risk': 'HIGH'
            },
            'red': {
                'class': 'red-alert',
                'icon': '🔴',
                'color': '#e74c3c',
                'title': 'RED ALERT',
                'message': 'CRITICAL SITUATION! Severe impact imminent. Immediate evacuation required. Deploy all emergency resources NOW!',
                'risk': 'CRITICAL'
            }
        }
        
        config = alert_config.get(prediction.lower(), alert_config['green'])
        confidence = max(proba) * 100
        
        # Main Alert Card
        st.markdown(f"""
        <div class='alert-card {config['class']}'>
            <div class='alert-icon'>{config['icon']}</div>
            <h1 class='alert-title'>{config['title']}</h1>
            <p class='alert-confidence'>Confidence Level: {confidence:.1f}%</p>
            <div style='margin-top: 30px; padding: 25px; background: rgba(255,255,255,0.2); border-radius: 15px; backdrop-filter: blur(10px);'>
                <p style='font-size: 1.3rem; line-height: 1.8; margin: 0;'>{config['message']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence Distribution
        st.markdown("<div class='input-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>📊 Confidence Distribution</h2>", unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Map colors to match alert levels: green, orange, red, yellow
        color_map = {
            'green': '#2ecc71',
            'orange': '#e67e22', 
            'red': '#e74c3c',
            'yellow': '#f1c40f'
        }
        colors = [color_map[cls.lower()] for cls in classes]
        
        fig.add_trace(go.Bar(
            x=classes,
            y=(proba * 100).tolist(),
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=[f"{p*100:.1f}%" for p in proba],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Probability: %{y:.1f}%<extra></extra>"
        ))
        
        fig.update_layout(
            title="Probability of Each Alert Level",
            xaxis_title="Alert Level",
            yaxis_title="Probability (%)",
            yaxis=dict(range=[0, 100]),
            height=420,
            showlegend=False,
            template="plotly_white",
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode="closest"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Impact Metrics
        st.markdown("<div class='input-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>📈 Impact Analysis</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        impact_score = magnitude * sig
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color: {config["color"]};'>{magnitude:.5f}</div>
                <div class='metric-label'>Magnitude</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color: {config["color"]};'>{impact_score:.0f}</div>
                <div class='metric-label'>Impact Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color: {config["color"]};'>{depth:.0f}</div>
                <div class='metric-label'>Depth (km)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color: {config["color"]};'>{config["risk"]}</div>
                <div class='metric-label'>Risk Level</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Detailed Parameters
        st.markdown("<div class='input-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>🔍 Detailed Parameters</h2>", unsafe_allow_html=True)
        
        params_df = pd.DataFrame({
            'Parameter': ['Magnitude', 'Depth', 'CDI', 'MMI', 'Significance', 'Impact Score', 'Depth/Magnitude Ratio'],
            'Value': [magnitude, depth, cdi, mmi, sig, impact_score, depth/(magnitude+1)],
            'Unit': ['Richter', 'km', 'Scale', 'Scale', 'Score', 'Computed', 'Ratio']
        })
        
        st.dataframe(
            params_df,
            use_container_width=True,
            hide_index=True,
            height=280
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Recommendations
        st.markdown(f"""
        <div class='recommendation-box' style='border-left-color: {config["color"]};'>
            <div class='recommendation-title'>💡 Emergency Response Recommendations</div>
            <div class='recommendation-text'>
                <strong>Immediate Actions:</strong><br>
                {config['message']}<br><br>
                <strong>Additional Measures:</strong><br>
                • Continuously monitor seismic activity updates<br>
                • Ensure communication channels remain operational<br>
                • Coordinate with local emergency management authorities<br>
                • Keep emergency kits and supplies readily accessible<br>
                • Document all observations and responses for post-event analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Timestamp - Generate at prediction time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"""
        <div style='text-align: center; color: #888; font-size: 0.9rem; margin-top: 30px;'>
            Prediction generated at: {current_time}
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Instructions when no prediction yet
        st.markdown("""
        <div class='input-card' style='text-align: center; padding: 60px 40px;'>
            <div style='font-size: 5rem; margin-bottom: 20px;'>🎯</div>
            <h2 style='color: #667eea; margin-bottom: 15px;'>Ready to Predict</h2>
            <p style='font-size: 1.2rem; color: #777; line-height: 1.8;'>
                Enter the earthquake parameters above and click<br>
                <strong>"PREDICT ALERT LEVEL"</strong> to get your analysis
            </p>
            <div style='margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 12px;'>
                <p style='color: #555; margin: 0;'>
                    💡 <em>Tip: Adjust the values carefully for accurate predictions</em>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("⚠️ Unable to load prediction model. Please ensure 'earthquake_model.pkl' exists in the directory.")

# Footer
st.markdown("""
<div class='footer'>
    <p style='font-size: 1.5rem; margin: 0; color: #667eea;'>🌍 <strong>ImpactSense</strong></p>
    <p class='footer-text' style='margin: 10px 0 0 0;'>
         Earthquake Impact Prediction System<br>
         Developed for Disaster Management & Emergency Response<br>
    </p>
</div>
""", unsafe_allow_html=True)
