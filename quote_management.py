import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Define the API details
BASE_URL = "https://positivity-tips.p.rapidapi.com/api/positivity"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "positivity-tips.p.rapidapi.com"
}


def fetch_data(endpoint):
    """
    Fetch data from the Positivity Tips API using the specified endpoint.
    Args:
        endpoint (str): The specific API endpoint to query (e.g., 'quote', 'wellness', 'affirmation').
    Returns:
        dict: The response data from the API, or an error message if the request fails.
    """
    if not isinstance(endpoint, str) or not endpoint:
        return {"error": "Invalid endpoint provided."}

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS)
        response.encoding = "utf-8"
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to the API. Please check your internet connection."}
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again later."}
    except requests.exceptions.RequestException as err:
        return {"error": f"An error occurred: {err}"}


def get_quote(max_length=120):
    """
    Fetch a random quote and ensure it is under the specified length.
    Args:
        max_length (int): The maximum allowed length for the quote.
        Default is 120 characters.
    Returns:
        str: A quote, or an error message if the quote is too long or fetching fails.
    """
    if not isinstance(max_length, int) or max_length <= 0:
        return "Invalid max_length provided. It must be a positive integer."

    data = fetch_data('quote')
    if 'quote' in data:
        quote = data['quote']
        # If quote is too long, return a message indicating that
        if len(quote) <= max_length:
            return quote
        else:
            return "Quote is too long, please try again later."
    return data.get('error', "An unexpected error occurred.")


def get_wellness_tip():
    """
    Fetch a random daily wellness tip to improve physical and mental well-being.
    Returns:
        str: A wellness tip, or an error message if the tip cannot be fetched.
    """
    data = fetch_data('wellness')
    if 'tip' in data:
        return data['tip']
    return data.get('error', "Could not fetch a wellness tip.")


def get_affirmation():
    """
    Fetch a random affirmation to empower the user.
    Returns:
        str: An affirmation, or an error message if the affirmation cannot be fetched.
    """
    data = fetch_data('affirmation')
    if 'affirmation' in data:
        return data['affirmation']
    return data.get('error', "Could not fetch an affirmation.")


# Example usage
print(get_quote())
print(get_wellness_tip())
print(get_affirmation())
