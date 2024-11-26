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
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.json()
    return {"error": f"Could not fetch data. Status code: {response.status_code}"}


def get_random_quote(max_length=120):
    data = fetch_data('quote')
    if 'quote' in data:
        quote = data['quote']
        # If quote is too long, try again
        if len(quote) <= max_length:
            return quote
        else:
            return "Quote is too long, please try again later."
    return data['error']


def get_wellness_tip():
    data = fetch_data('wellness')
    if 'tip' in data:
        return data['tip']
    return data.get('error', "Could not fetch a wellness tip.")


def get_affirmation():
    data = fetch_data('affirmation')
    if 'affirmation' in data:
        return data['affirmation']
    return data.get('error', "Could not fetch an affirmation.")


# Example usage
print(get_random_quote())
print(get_wellness_tip())
print(get_affirmation())
