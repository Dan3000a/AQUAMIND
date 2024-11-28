import json


def fetch_phone_numbers_from_json(file_path, key_name='phone_number'):
    """
    Fetch a list of phone numbers from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing phone numbers.
        key_name (str): The key to extract phone numbers from (default is 'phone_number').

    Returns:
        list: A list of valid phone numbers.
    """
    phone_numbers = []

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON data

            # Assuming the data is a list of dictionaries
            for item in data:
                if key_name in item:
                    phone_number = str(item[key_name]).strip()
                    phone_numbers.append(phone_number)
                else:
                    print(f"Warning: Key '{key_name}' not found in {item}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return phone_numbers


# Example usage:
file_path = 'user_data.json'  # Ensure this file exists in your directory
numbers = fetch_phone_numbers_from_json(file_path)
print(numbers)
