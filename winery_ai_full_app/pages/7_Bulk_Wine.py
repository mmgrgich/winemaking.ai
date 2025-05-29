
import streamlit as st
from vintrace_api import get_bulk_wine

st.set_page_config(page_title="Bulk Wine", layout="wide")
st.title("📦 Live Bulk Wine Inventory")

with st.spinner("Fetching bulk wine data..."):
    data = get_bulk_wine()
    if data and isinstance(data, list):
        st.success(f"{len(data)} bulk wine records loaded")
        st.dataframe(data)
    else:
        st.warning("No bulk wine data found or API error.")
