
import streamlit as st
from vintrace_api import get_movements
from datetime import date

st.set_page_config(page_title="Movement Logs", layout="wide")
st.title("🚚 Wine Movement Logs")

start_date = st.date_input("Start Date", value=date.today())
end_date = st.date_input("End Date", value=date.today())

if st.button("Fetch Movements"):
    with st.spinner("Fetching movement data..."):
        data = get_movements(start_date=start_date.isoformat(), end_date=end_date.isoformat())
        if data and isinstance(data, list):
            st.success(f"{len(data)} movements found")
            st.dataframe(data)
        else:
            st.warning("No movements found or API error.")
