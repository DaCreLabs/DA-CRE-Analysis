import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import secrets
import string
import time

# Page Configuration
st.set_page_config(
    page_title="DA-CRE Analysis Platform",
    page_icon="🪄📊",
    layout="wide"
)

# Custom Styling (Hover/Loading Animation & CSS Theme)
st.markdown("""
    <style>
    /* Hover Loading Card Styling */
    .loading-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: pulse 2s infinite;
        margin-bottom: 2rem;
    }
    .loading-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }
    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    /* Main Banner */
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

# Helper function to generate secure password
def generate_strong_password(length=12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Initialize Session State Variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'declined_suggested' not in st.session_state:
    st.session_state['declined_suggested'] = False
if 'suggested_pw' not in st.session_state:
    st.session_state['suggested_pw'] = generate_strong_password()


# --- SIGN-UP SCREEN ---
if not st.session_state['authenticated']:
    
    # Animated Hover Banner
    st.markdown("""
        <div class="loading-card">
            <h1>DA-CRE Analysis Platform</h1>
            <p style="font-size: 1.2rem;">✨ Initializing AI Engine... Please Sign Up to Continue</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("📝 Create Your Account")
        
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        email = st.text_input("Email Address")

        password_to_use = ""

        # Email Validation Check
        email_error = False
        if email and "@" not in email:
            st.error("❌ Invalid Email: Your email address must contain an '@' symbol.")
            email_error = True

        # Password Logic (Suggested vs Custom)
        st.write("---")
        if not st.session_state['declined_suggested']:
            st.info(f"💡 **Suggested Secure Password:** `{st.session_state['suggested_pw']}`")
            
            c_acc, c_dec = st.columns(2)
            with c_acc:
                accept_suggested = st.button("Use Suggested Password")
                if accept_suggested:
                    password_to_use = st.session_state['suggested_pw']
            with c_dec:
                if st.button("Decline & Set My Own Password"):
                    st.session_state['declined_suggested'] = True
                    st.rerun()
        else:
            password_to_use = st.text_input("Set Your Password", type="password")
            if st.button("Re-enable Suggested Password"):
                st.session_state['declined_suggested'] = False
                st.rerun()

        st.write("---")
        
        # Submit Signup Form
        if st.button("Complete Sign Up & Access App"):
            if not first_name:
                st.warning("Please enter your First Name.")
            elif not email or email_error:
                st.warning("Please enter a valid Email Address containing '@'.")
            elif not password_to_use:
                st.warning("Please choose or accept a password.")
            else:
                # Store User Information
                st.session_state['user_name'] = f"{first_name} {middle_name}".strip()
                st.session_state['authenticated'] = True
                st.success("Registration Successful! Redirecting...")
                time.sleep(1)
                st.rerun()

# --- MAIN APPLICATION (LOCKED UNTIL SIGN-UP) ---
else:
    # Navigation Sidebar with Logout Button
    st.sidebar.title(f"Welcome, {st.session_state.get('user_name', 'User')}!")
    if st.sidebar.button("🔒 Sign Out"):
        st.session_state['authenticated'] = False
        st.session_state['declined_suggested'] = False
        st.rerun()

    st.markdown("""
        <div class="main-header">
            <h1>DA-CRE Analysis Platform</h1>
            <p>AI-Powered Commercial Real Estate & Data Analytics Engine</p>
        </div>
    """, unsafe_allow_html=True)

    app_mode = st.sidebar.radio(
        "Choose Module",
        ["🌐 1. Web Data Extractor", "📁 2. File Upload (CSV/Excel)", "🧹 3. Data Cleaning", "📊 4. Visual Analytics"]
    )

    # MODULE 1: WEB SCRAPER
    if app_mode == "🌐 1. Web Data Extractor":
        st.subheader("🌐 Website Data Extraction")
        st.write("Paste any website URL containing tables to automatically extract and convert data.")
        
        url_input = st.text_input("Enter Website URL:", "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
        
        if st.button("Extract Tables"):
            if url_input:
                try:
                    with st.spinner("Extracting data tables from URL..."):
                        tables = pd.read_html(url_input)
                        st.success(f"Successfully found {len(tables)} tables on the webpage!")
                        
                        for i, df in enumerate(tables):
                            with st.expander(f"Table {i+1} ({df.shape[0]} rows, {df.shape[1]} columns)"):
                                st.dataframe(df)
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label=f"Download Table {i+1} as CSV",
                                    data=csv,
                                    file_name=f'extracted_table_{i+1}.csv',
                                    mime='text/csv'
                                )
                except Exception as e:
                    st.error(f"Could not extract tables: {e}. Ensure the URL contains valid public HTML tables.")

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
            except Exception as e:
                st.error(f"Error loading file: {e}")

    # MODULE 3: DATA CLEANING
    elif app_mode == "🧹 3. Data Cleaning":
        st.subheader("🧹 Automated Data Cleaning Engine")
        
        if 'current_data' in st.session_state:
            df = st.session_state['current_data']
            st.dataframe(df.head())
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Remove Duplicate Rows"):
                    df_cleaned = df.drop_duplicates()
                    st.session_state['current_data'] = df_cleaned
                    st.success(f"Removed duplicates! New count: {df_cleaned.shape[0]}")
            with c2:
                if st.button("Drop Missing (NaN) Values"):
                    df_cleaned = df.dropna()
                    st.session_state['current_data'] = df_cleaned
                    st.success(f"Dropped missing values! New count: {df_cleaned.shape[0]}")
        else:
            st.info("Please upload a file in Module 2 first.")

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
                st.warning("Dataset needs at least one numeric column for chart creation.")
        else:
            st.info("Upload data in Module 2 or extract a table in Module 1 to plot charts.")
