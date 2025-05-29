import requests
import streamlit as st

BASE_URL = "https://api.vintrace.com/api/v1"

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def get_lab_results(wine_id=None, lot_code=None):
    params = {}
    if wine_id:
        params["wineId"] = wine_id
    if lot_code:
        params["lotCode"] = lot_code

    response = requests.get(f"{BASE_URL}/lab-results", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch lab results: {response.status_code}")
        return None

def get_bulk_wine():
    response = requests.get(f"{BASE_URL}/bulk-wine", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch bulk wine: {response.status_code}")
        return None

def get_movements(start_date=None, end_date=None):
    params = {}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date

    response = requests.get(f"{BASE_URL}/movements", headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch movements: {response.status_code}")
        return None
