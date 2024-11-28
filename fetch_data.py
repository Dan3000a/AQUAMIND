import requests
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Define categories for quotes
categories = ['inspirational', 'love', 'life', 'friendship', 'success', 'health', 'fitness'
              'happiness']


def get_random_quote(max_length=120):
    """
    Fetch a random quote from the API, ensuring it doesn't exceed the maximum length.
    Args:
        max_length (int): Maximum allowed length for the quote.
    Returns:
        str or dict: The quote if found, or an error message.
    """

    if not isinstance(max_length, int) or max_length <= 0:
        return "Invalid max_length provided. It must be a positive integer."

    while True:
        category = random.choice(categories)
        api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"

        try:
            response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
            response.encoding = "utf-8"

            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            quotes = response.json()
            if quotes:
                quote_text = quotes[0]['quote']
                if len(quote_text) <= max_length:
                    return quote_text

        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.ConnectionError:
            return {"error": "Unable to connect to the API. Please check your internet connection."}
        except requests.exceptions.Timeout:
            return {"error": "The request timed out. Please try again later."}
        except requests.exceptions.RequestException as err:
            return {"error": f"An error occurred: {err}"}

