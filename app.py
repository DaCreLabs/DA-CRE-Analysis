import pandas as pd

def extract_tables_from_url(url):
    """
    DA-CRE Analysis - Phase 1: Web Data Extractor
    Takes a website URL and extracts all table data into structured pandas DataFrames.
    """
    print(f"Fetching data from: {url}")
    try:
        tables = pd.read_html(url)
        print(f"Successfully extracted {len(tables)} table(s)!")
        return tables
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

if __name__ == "__main__":
    print("--- DA-CRE Analysis Engine Started ---")
    test_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    extracted_data = extract_tables_from_url(test_url)
