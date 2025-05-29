import requests
import streamlit as st

BASE_URL = "https://us42.vintrace.net/grgich/api/v9"

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def get_bulk_wine():
    response = requests.get(f"{BASE_URL}/vessel", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch bulk wine: {response.status_code} {response.text}")
        return None

def get_lab_results(wine_id=None, lot_code=None):
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

def get_movements(params=None):
    """Fetch movement logs from Vintrace."""
    if params is None:
        params = {}
    response = requests.get(f"{BASE_URL}/movements", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch movements: {response.status_code} {response.text}")
        return None
