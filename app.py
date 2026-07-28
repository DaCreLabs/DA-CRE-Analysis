import streamlit as st
import pandas as pd

st.set_page_config(page_title="DA-CRE Analysis", page_icon="📊", layout="wide")

st.title("📊 DA-CRE Analysis")
st.subheader("AI-Powered Data Analytics & Extraction Platform")

st.markdown("---")

# Navigation sidebar
st.sidebar.title("DA-CRE Navigation")
option = st.sidebar.radio("Choose a Tool:", ["🌐 Web Data Extractor", "🧹 Clean Data", "📈 Analyze Data"])

if option == "🌐 Web Data Extractor":
    st.header("🌐 Website Data Extractor")
    st.write("Enter any public website URL containing data tables to extract them automatically.")
    
    url = st.text_input("Enter Web URL:", value="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")
    
    if st.button("Extract Data"):
        if url:
            try:
                with st.spinner("Extracting tables..."):
                    tables = pd.read_html(url)
                    st.success(f"Successfully extracted {len(tables)} table(s)!")
                    
                    for idx, table in enumerate(tables):
                        st.write(f"### Table {idx + 1}")
                        st.dataframe(table)
                        
                        # Download button for CSV
                        csv = table.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=f"📥 Download Table {idx + 1} as CSV",
                            data=csv,
                            file_name=f"dacre_extracted_table_{idx + 1}.csv",
                            mime="text/csv"
                        )
            except Exception as e:
                st.error(f"Failed to extract data: {e}")
        else:
            st.warning("Please enter a valid URL.")

elif option == "🧹 Clean Data":
    st.header("🧹 Data Cleaning Suite")
    st.info("Feature coming next in Phase 2!")

elif option == "📈 Analyze Data":
    st.header("📈 Data Analysis Engine")
    st.info("Feature coming in Phase 3!")
