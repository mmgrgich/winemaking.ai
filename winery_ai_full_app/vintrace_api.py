import requests
import streamlit as st

BASE_URL = "https://us42.vintrace.net/grgich/api/v6"  # Or v9 if needed

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def safe_api_call(url, params=None, description="API call"):
    """Unified error-handling wrapper for API GET calls."""
    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error(f"Unauthorized: Check your API token for {description}.")
        elif response.status_code == 403:
            st.error(f"Forbidden: You do not have access to this resource ({description}).")
        elif response.status_code == 404:
            st.warning(f"Not found (404): The endpoint or resource does not exist for {description}.")
        elif response.status_code == 500:
            st.error(f"Server error (500) during {description}. Please try again later.")
        else:
            st.error(f"Error {response.status_code} on {description}: {response.text[:200]}")
    except requests.exceptions.Timeout:
        st.error(f"Request timed out while attempting {description}.")
    except requests.exceptions.ConnectionError:
        st.error(f"Connection error while attempting {description}.")
    except Exception as e:
        st.error(f"Unexpected error during {description}: {e}")
    return None

def get_movements(start_date=None, end_date=None):
    """Fetch planned/completed wine movements, optionally filtered by date."""
    params = {}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    url = f"{BASE_URL}/movements"
    return safe_api_call(url, params, description="fetching movements")

def get_bulk_wine():
    """Fetch all bulk wine batches."""
    url = f"{BASE_URL}/bulk-wine"
    return safe_api_call(url, description="fetching bulk wine batches")

def get_lab_results(wine_id=None, lot_code=None):
    """Fetch recent lab results, optionally filtered by batch/lot code."""
    params = {}
    if wine_id:
        params["wineId"] = wine_id
    if lot_code:
        params["lotCode"] = lot_code
    url = f"{BASE_URL}/lab-results"
    return safe_api_call(url, params, description="fetching lab results")
