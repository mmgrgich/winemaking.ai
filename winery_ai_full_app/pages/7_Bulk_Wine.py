import streamlit as st
from vintrace_api import get_bulk_wine
import pandas as pd
import requests

st.set_page_config(page_title="Bulk Wine", layout="wide")
st.title("📦 Live Bulk Wine Inventory")

# Fetch the API token from secrets
api_token = st.secrets.get("vintrace_api_token")

with st.spinner("Fetching bulk wine data..."):
    data = get_bulk_wine()
    if data and isinstance(data, list):
        df = pd.DataFrame(data)
        st.success(f"{len(df)} bulk wine records loaded")

        # --- SEARCH FILTER ---
        search = st.text_input("🔎 Search bulk wine (by any column):").strip().lower()
        if search:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search).any(), axis=1)]
        else:
            filtered_df = df

        st.dataframe(filtered_df)
    else:
        st.warning("No bulk wine data found or API error.")

        url = "https://us42.vintrace.net/grgich/api/v6/products/list"
        querystring = {"skipMetrics": "true"}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_token}"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    st.write("API raw data:", json_data)
                except requests.exceptions.JSONDecodeError:
                    st.error("API response is not valid JSON.")
                    st.text("Raw response:")
                    st.text(response.text)
            else:
                st.error(f"API returned status code {response.status_code}")
                st.text("Raw response:")
                st.text(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
