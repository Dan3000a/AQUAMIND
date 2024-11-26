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


def get_random_quote():
    response = requests.get(f"{BASE_URL}/quote", headers=HEADERS)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.json().get('quote', "Stay inspired!")
    return f"Could not fetch a quote. Status code: {response.status_code}"


def get_wellness_tip():
    response = requests.get(f"{BASE_URL}/wellness", headers=HEADERS)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.json().get('tip', "Take care of your health!")
    return f"Could not fetch a wellness tip. Status code: {response.status_code}"


def get_affirmation():
    response = requests.get(f"{BASE_URL}/affirmation", headers=HEADERS)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.json().get('affirmation', "You are capable!")
    return f"Could not fetch an affirmation. Status code: {response.status_code}"


# Example usage
print(get_random_quote())
print(get_wellness_tip())
print(get_affirmation())
