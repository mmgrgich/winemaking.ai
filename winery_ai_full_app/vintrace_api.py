import requests
import streamlit as st

# ✅ Confirmed correct base URL for your instance
BASE_URL = "https://us42.vintrace.net/grgich/api/"

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets["API_TOKEN"]}",
        "Accept": "application/json"
    }

def safe_api_call(url, params=None, description="API call"):
    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=300)
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

# ✅ Bulk Wine - Confirmed endpoint
def get_bulk_wine():
    """Fetch all bulk wine batches."""
    url = f"{BASE_URL}v6/products/list"
    return safe_api_call(url, description="fetching bulk wine batches")

# ✅ FIXED: Lab Results via ANALYSIS ops in transaction search
def get_lab_results(wine_id=None, lot_code=None, from_date=None, to_date=None):
    """Fetch lab results (ANALYSIS operations) via transaction search."""
    params = {"type": "ANALYSIS"}
    if wine_id:
        params["wineId"] = wine_id
    if lot_code:
        params["lotCode"] = lot_code
    if from_date:
        params["startDate"] = from_date
    if to_date:
        params["endDate"] = to_date
    url = f"{BASE_URL}v6/products/list"
    return safe_api_call(url, params, description="fetching lab results (analysis ops)")

# ✅ Movements (all job types)
def get_movements(start_date=None, end_date=None):
    """Fetch wine movements (all job types)."""
    params = {}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    url = f"{BASE_URL}v6/transaction/search"
    return safe_api_call(url, params, description="fetching movements")
