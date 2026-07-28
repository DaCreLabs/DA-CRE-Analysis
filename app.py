import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# Page Configuration
st.set_page_config(
    page_title="DA-CRE Analysis Platform",
    page_icon="🪄📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.8rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
    <div class="main-header">
        <h1>DA-CRE Analysis Platform</h1>
        <p>AI-Powered Commercial Real Estate & Data Analytics Engine</p>
    </div>
""", unsafe_allow_html=True)

# Navigation Sidebar
st.sidebar.title("DA-CRE Navigation")
app_mode = st.sidebar.radio(
    "Choose Module",
    ["🌐 1. Web Data Extractor", "📁 2. File Upload (CSV/Excel)", "🧹 3. Data Cleaning", "📊 4. Visual Analytics"]
)

# MODULE 1: WEB SCRAPER
if app_mode == "🌐 1. Web Data Extractor":
    st.subheader("🌐 Website Data Extraction")
    st.write("Paste any website URL containing tables to automatically extract and convert data.")
    
    url_input = st.text_input("Enter Website URL (e.g., https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue):")
    
    if st.button("Extract Tables"):
        if url_input:
            try:
                with st.spinner("Extracting data tables from URL..."):
                    tables = pd.read_html(url_input)
                    st.success(f"Successfully found {len(tables)} tables on the webpage!")
                    
                    # Display extracted tables
                    for i, df in enumerate(tables):
                        with st.expander(f"Table {i+1} ({df.shape[0]} rows, {df.shape[1]} columns)"):
                            st.dataframe(df)
                            
                            # Download option for extracted table
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label=f"Download Table {i+1} as CSV",
                                data=csv,
                                file_name=f'extracted_table_{i+1}.csv',
                                mime='text/csv'
                            )
            except Exception as e:
                st.error(f"Could not extract tables: {e}. Please ensure the URL contains valid public HTML tables.")
        else:
            st.warning("Please enter a valid URL.")

# MODULE 2: FILE UPLOADER
elif app_mode == "📁 2. File Upload (CSV/Excel)":
    st.subheader("📁 Upload Local Data Files")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state['current_data'] = df
            st.success(f"Successfully loaded {uploaded_file.name}!")
            st.dataframe(df.head(10))
            st.info(f"Dataset shape: {df.shape[0]} rows and {df.shape[1]} columns.")
        except Exception as e:
            st.error(f"Error loading file: {e}")

# MODULE 3: DATA CLEANING
elif app_mode == "🧹 3. Data Cleaning":
    st.subheader("🧹 Automated Data Cleaning Engine")
    
    if 'current_data' in st.session_state:
        df = st.session_state['current_data']
        st.write("Current Dataset Preview:")
        st.dataframe(df.head())
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Remove Duplicate Rows"):
                df_cleaned = df.drop_duplicates()
                st.session_state['current_data'] = df_cleaned
                st.success(f"Removed duplicates! New row count: {df_cleaned.shape[0]}")
        
        with c2:
            if st.button("Drop Missing (NaN) Values"):
                df_cleaned = df.dropna()
                st.session_state['current_data'] = df_cleaned
                st.success(f"Dropped missing values! New row count: {df_cleaned.shape[0]}")
    else:
        st.info("Please upload a file in '2. File Upload' first to clean your data.")

# MODULE 4: VISUAL ANALYTICS
elif app_mode == "📊 4. Visual Analytics":
    st.subheader("📊 Visual Analytics Engine")
    
    if 'current_data' in st.session_state:
        df = st.session_state['current_data']
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        all_cols = df.columns.tolist()
        
        if numeric_cols and len(all_cols) >= 2:
            x_axis = st.selectbox("Select X-Axis", all_cols)
            y_axis = st.selectbox("Select Y-Axis (Numeric)", numeric_cols)
            
            chart_type = st.radio("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
            
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
            else:
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dataset needs at least one numeric column to generate automated visualizations.")
    else:
        st.info("Please upload data in Module 2 or extract a table in Module 1 to visualize.")
