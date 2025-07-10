import requests
import streamlit as st

# Use your correct base path (confirm no extra "/grgich" unless Dev Tools shows it!)
BASE_URL = "https://us42.vintrace.net/api/"

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def safe_api_call(url, params=None, description="API call"):
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

def get_bulk_wine():
    """Fetch all bulk wine batches."""
    url = f"{BASE_URL}v7/wine-batch"
    return safe_api_call(url, description="fetching bulk wine batches")

def get_lab_results(wine_id=None, lot_code=None, from_date=None, to_date=None):
    """Fetch lab results filtered by wine ID or lot code and optional dates."""
    params = {}
    if wine_id:
        params["wineId"] = wine_id
    if lot_code:
        params["lotCode"] = lot_code
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    url = f"{BASE_URL}v7/lab-result"
    return safe_api_call(url, params, description="fetching lab results")

def get_movements(start_date=None, end_date=None):
    """Fetch wine movements (jobs/transactions)."""
    params = {}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    url = f"{BASE_URL}v6/transaction/search"
    return safe_api_call(url, params, description="fetching movements")

