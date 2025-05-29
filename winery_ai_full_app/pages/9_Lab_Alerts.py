
import streamlit as st
import pandas as pd
from vintrace_api import get_lab_results

st.set_page_config(page_title="Lab Alerts", layout="wide")
st.title("🔔 Live Lab Alerts")

lot_code = st.text_input("Enter Lot Code")

CRITICAL_THRESHOLDS = {
    "pH": (3.0, 3.7),
    "VA": (0.0, 0.7),
    "SO2": (20, 60)
}

def check_alerts(row):
    alerts = []
    for param, (low, high) in CRITICAL_THRESHOLDS.items():
        value = row.get(param)
        if isinstance(value, (int, float)):
            if value < low or value > high:
                alerts.append(f"{param} out of range")
    return ", ".join(alerts)

if lot_code:
    data = get_lab_results(lot_code=lot_code)
    if data and isinstance(data, list):
        df = pd.DataFrame(data)
        df["Alerts"] = df.apply(check_alerts, axis=1)
        st.subheader("⚠️ Lab Alerts")
        st.dataframe(df[df["Alerts"] != ""])
    else:
        st.warning("No lab data or API error.")
