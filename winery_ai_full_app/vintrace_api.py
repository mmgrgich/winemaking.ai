import requests
import streamlit as st

# Set this to your actual vintrace domain, e.g. "acme.vintrace.com"
BASE_URL = "https://us42.vintrace.net/grgich/api/v9"

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def get_bulk_wine():
    """Fetch bulk wine data from Vintrace."""
    response = requests.get(f"{BASE_URL}/vessel", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch bulk wine: {response.status_code} {response.text}")
        return None

def get_lab_results(wine_id=None, lot_code=None):
    """Fetch lab results from Vintrace."""
    params = {}
    if wine_id:
        params["wineId"] = wine_id
    if lot_code:
        params["lotCode"] = lot_code

    response = requests.get(f"{BASE_URL}/report/vessel-details-report", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch lab results: {response.status_code} {response.text}")
        return None

# Example usage (uncomment in your Streamlit app as needed):
#
# bulk_wine_data = get_bulk_wine()
# lab_results_data = get_lab_results()
# st.write("Bulk Wine:", bulk_wine_data)
# st.write("Lab Results:", lab_results_data)
