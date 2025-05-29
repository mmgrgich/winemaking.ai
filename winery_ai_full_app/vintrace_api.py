import requests
import streamlit as st
import re
import time

BASE_URL = "https://us42.vintrace.net/grgich/api/v7"  # Change to v9 if needed

def get_headers():
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Accept": "application/json"
    }

def extract_paths(text):
    """Extract possible endpoint paths from a JSON/text response string."""
    # Find likely API paths such as "/something" or "/something/else"
    paths = set(re.findall(r'["\'](/[^"\',\s\]\}]*)', text))
    # Remove query string and fragment
    return set(p.split('?')[0].split('#')[0] for p in paths)

def is_valid_path(path):
    # Ignore links to docs, images, scripts, etc.
    return path.startswith('/') and not any(
        path.endswith(ext)
        for ext in ['.js', '.css', '.png', '.jpg', '.ico', '.html', '.svg']
    )

def restful_guesses(path, sample_ids=["1", "999", "test"]):
    """Guess common RESTful subpaths based on the path."""
    guesses = []
    # Guess ID-based sub-resources for collection endpoints
    if path.endswith('s'):  # e.g. /vessels, /movements
        for sample_id in sample_ids:
            guesses.append(f"{path}/{sample_id}")
            guesses.append(f"{path}/{sample_id}/lab-results")
            guesses.append(f"{path}/{sample_id}/movements")
            guesses.append(f"{path}/{sample_id}/history")
    return guesses

def aggressive_discover(start_endpoint="", visited=None, depth=0, max_depth=4):
    """Aggressively discover endpoints, following links and guessing RESTful paths."""
    if visited is None:
        visited = set()
    if depth > max_depth:
        return visited
    url = f"{BASE_URL}{start_endpoint}"
    if url in visited:
        return visited
    try:
        resp = requests.get(url, headers=get_headers(), timeout=10)
        st.write(f"Probing {url} — status: {resp.status_code}")
        if resp.status_code == 404:
            return visited
        visited.add(url)
        text = resp.text
        # Extract new paths from response
        new_paths = {p for p in extract_paths(text) if is_valid_path(p)}
        # Add guessed RESTful subpaths
        for g in restful_guesses(start_endpoint):
            new_paths.add(g)
        # Crawl new paths
        for path in new_paths:
            # Only crawl relative paths within the API
            if path.startswith("/"):
                full_url = BASE_URL + path if not path.startswith(BASE_URL) else path
                if full_url not in visited:
                    # Respect API rate limits
                    time.sleep(0.3)
                    aggressive_discover(path, visited, depth+1, max_depth)
    except Exception as e:
        st.error(f"Error querying {url}: {e}")
    return visited

def run_aggressive_discover():
    st.write("Aggressively discovering endpoints from API root (may take a few minutes)...")
    endpoints_found = aggressive_discover("", set(), 0, max_depth=4)
    st.write("Discovered endpoints (not 404):")
    st.json(sorted(list(endpoints_found)))
