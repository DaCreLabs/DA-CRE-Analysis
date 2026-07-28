import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# Set page config
st.set_page_config(
    page_title="DA-CRE Analysis Platform",
    page_icon="📊",
    layout="wide"
)

# Custom Styling - Dynamic Blue Theme
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .profile-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1e3c72;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# Top Title Banner
st.markdown("""
    <div class="main-header">
        <h1>DA-CRE Analysis Platform</h1>
        <p style="font-size: 1.2rem; margin-bottom: 0;">AI-Powered Commercial Real Estate & Data Analytics</p>
    </div>
""", unsafe_allow_html=True)

# Profile Section Header
col_img, col_info = st.columns([1, 3])

with col_img:
    img_path = "david_profile.png"
    if os.path.exists(img_path):
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
    else:
        st.info("📌 Upload 'david_profile.png' to show profile picture")

with col_info:
    st.markdown("""
        <div class="profile-card">
            <h2 style="color: #1e3c72; margin-top:0;">Uchechukwu David Emenike</h2>
            <h4 style="color: #495057;">Lead Data Analyst & CRE Specialist</h4>
            <p>Welcome to the <b>DA-CRE Analysis Platform</b>. This interactive system automates data collection, 
            cleaning, visualization, and strategic reporting for market intelligence and asset evaluation.</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Interactive Section
st.subheader("📈 Dynamic Analytics Dashboard")

# Sample Interactive Layout
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Properties Analyzed", "1,240", "+12%")
c2.metric("Avg Cap Rate", "6.8%", "+0.4%")
c3.metric("Market Occupancy", "94.2%", "-0.8%")
c4.metric("Pipeline Value", "$42.5M", "+18%")

# Chart Layout
col_chart1, col_chart2 = st.columns(2)

df = pd.DataFrame({
    'Category': ['Office', 'Retail', 'Industrial', 'Multi-Family'],
    'Value': [35, 20, 30, 15]
})

with col_chart1:
    fig1 = px.pie(df, values='Value', names='Category', title='Portfolio Allocation', color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    fig2 = px.bar(df, x='Category', y='Value', title='Property Distribution', color='Value', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)
