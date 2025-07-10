import streamlit as st
from vintrace_api import get_bulk_wine
import requests

st.set_page_config(page_title="Bulk Wine", layout="wide")
st.title("📦 Live Bulk Wine Inventory")

# Get the API token from Streamlit secrets
api_token = st.secrets.get("vintrace_api_token")  # Replace with your actual secret key name

with st.spinner("Fetching bulk wine data..."):
    data = get_bulk_wine()
    if data and isinstance(data, list):
        st.success(f"{len(data)} bulk wine records loaded")
        st.dataframe(data)
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
