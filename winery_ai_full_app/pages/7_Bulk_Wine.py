import streamlit as st
from vintrace_api import get_bulk_wine
import pandas as pd

st.set_page_config(page_title="Bulk Wine", layout="wide")
st.title("📦 Live Bulk Wine Inventory")

# --- Fetch Data ---
with st.spinner("Fetching bulk wine data..."):
    raw_data = get_bulk_wine()

# --- Parse Response ---
records = []
if raw_data:
    if isinstance(raw_data, dict) and "content" in raw_data:
        records = raw_data["content"]
    elif isinstance(raw_data, list):
        records = raw_data

if not records:
    st.warning("⚠️ No bulk wine data found or API error.")
    st.stop()

# --- Convert to DataFrame ---
df = pd.json_normalize(records)

# --- Clean Column Names ---
df.columns = df.columns.str.replace(r"\.", "_", regex=True).str.replace("_", " ").str.title()

# --- Quick Metrics ---
st.markdown("### 🧮 Inventory Overview")
col1, col2 = st.columns(2)
col1.metric("Total Batches", len(df))
col2.metric("Unique Lot Codes", df["Lot Code"].nunique() if "Lot Code" in df.columns else "—")

# --- Search Filter ---
search_term = st.text_input("🔍 Search bulk wine (any column):").strip().lower()
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]
else:
    filtered_df = df

# --- Show Table ---
st.markdown("### 📋 Bulk Wine Table")
st.dataframe(filtered_df, use_container_width=True)

# --- Download Button ---
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", csv, "bulk_wine_inventory.csv", "text/csv")

# --- Optional: JSON Preview for Debugging ---
with st.expander("🔧 Show Raw JSON Records"):
    st.json(records)
