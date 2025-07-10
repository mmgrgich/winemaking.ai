
import streamlit as st
from vintrace_api import get_bulk_wine
import requests 

st.set_page_config(page_title="Bulk Wine", layout="wide")
st.title("📦 Live Bulk Wine Inventory")

with st.spinner("Fetching bulk wine data..."):
    data = get_bulk_wine()
    if data and isinstance(data, list):
        st.success(f"{len(data)} bulk wine records loaded")
        st.dataframe(data)
    else:
        st.warning("No bulk wine data found or API error.")
        url = "https://us42.vintrace.net/grgich/api/v6/products/list"

querystring = {"skipMetrics":"true"}

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
