import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('API_KEY')  # API key for fetching quotes

# Categories for quotes
categories = ['inspirational', 'love', 'life', 'success', 'fitness', 'health']


def get_random_quote(max_length=150):
    """
    Fetch a random quote from the API.
    Args:
        max_length (int): Maximum allowed quote length.
    Returns:
        str or dict: Random quote or error message.
    """
    while True:
        category = random.choice(categories)  # Randomly pick a category
        url = f"https://api.api-ninjas.com/v1/quotes?category={category}"

        try:
            response = requests.get(url, headers={'X-Api-Key': API_KEY})
            response.raise_for_status()  # Raise exception for bad responses

            quotes = response.json()  # Parse JSON response
            if quotes:
                quote_text = quotes[0]['quote']
                if len(quote_text) <= max_length:
                    return quote_text  # Return valid quote
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}  # Handle exceptions