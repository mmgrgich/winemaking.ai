
import streamlit as st
from vintrace_api import get_lab_results

st.set_page_config(page_title="Real-Time Lab Results", layout="wide")
st.title("🧪 Real-Time Lab Results from Vintrace")

lot_code = st.text_input("Enter Lot Code to Search", "")

if lot_code:
    with st.spinner("Fetching lab results..."):
        lab_data = get_lab_results(lot_code=lot_code)
        if lab_data and isinstance(lab_data, list) and len(lab_data) > 0:
            st.success(f"Found {len(lab_data)} lab results")
            st.dataframe(lab_data)
        else:
            st.warning("No lab results found for that lot code.")
else:
    st.info("Enter a lot code above to view lab data in real time.")
