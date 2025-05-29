import requests
import streamlit as st

# Set the correct Vintrace API version and URL for your instance
BASE_URL = "https://us42.vintrace.net/grgich/api/v7"  # Or v9 if available

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def get_vessels():
    """Fetch all vessels (tanks, barrels, etc)."""
    response = requests.get(f"{BASE_URL}/vessels", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch vessels: {response.status_code} {response.text}")
        return None

def get_bulk_wine():
    """Fetch all bulk wine batches."""
    response = requests.get(f"{BASE_URL}/bulk-wine", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch bulk wine: {response.status_code} {response.text}")
        return None

def get_movements(start_date=None, end_date=None):
    """Fetch planned/completed wine movements, optionally filtered by date."""
    params = {}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    response = requests.get(f"{BASE_URL}/movements", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch movements: {response.status_code} {response.text}")
        return None

def get_lab_results(batch_code=None):
    """Fetch recent lab results, optionally filtered by batch code."""
    params = {}
    if batch_code:
        params["batchCode"] = batch_code
    response = requests.get(f"{BASE_URL}/lab-results", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch lab results: {response.status_code} {response.text}")
        return None

def get_inventory(item_type=None):
    """Fetch inventory items, optionally filter by item type (e.g. 'bottles', 'closures')."""
    params = {}
    if item_type:
        params["type"] = item_type
    response = requests.get(f"{BASE_URL}/inventory", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch inventory: {response.status_code} {response.text}")
        return None
