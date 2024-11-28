import json
import os
from water_intake import calculate_daily_intake

# Constants for file paths and modes
USER_DATA_FILE_PATH = "user_data.json"


def load_user_data():
    """
    Load user data from the JSON file.
    Tries to read the user data from the specified JSON file. If the file does not
    exist or is corrupted, it returns an empty list of users.
    Returns:
        dict: A dictionary with a list of users. Example: {"users": []}.
    """
    if not os.path.exists(USER_DATA_FILE_PATH):
        return {"users": []}  # Initialize an empty list for users if the file does not exist

    try:
        with open(USER_DATA_FILE_PATH, 'r') as user_file:
            return json.load(user_file)
    except json.JSONDecodeError:
        print("Error: Corrupted user data file.")
        return {"users": []}
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return {"users": []}


def save_user_data(user_data):
    """
    Save the updated user data to the JSON file.
    Attempts to save the updated user data to the specified JSON file.
    Args:
        user_data (dict): A dictionary containing user data to be saved.
    Returns:
        None
    """
    try:
        with open(USER_DATA_FILE_PATH, 'w') as user_file:
            json.dump(user_data, user_file, indent=4)
    except IOError as io_error:
        print(f"File I/O error: {str(io_error)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def register_user(username, phone_number, gender, age, weight):
    """
    Register a new user and calculate their daily water intake target.
    Validates user input, calculates the daily water intake target, and adds the
    user to the system. The user data is saved to the user data file.
    Args:
        username (str): The username for the new user.
        phone_number (str): The user's phone number.
        gender (str): The user's gender ('male' or 'female').
        age (int): The user's age.
        weight (float): The user's weight in kilograms.
    Returns:
        str: A message indicating success or the error encountered.
    """
    # Input validation
    if gender not in ['male', 'female']:
        return "Invalid gender. Please enter 'male' or 'female'."

    if not (0 < age < 150):
        return "Invalid age. Please enter a valid age."

    if weight <= 0:
        return "Invalid weight. Please enter a positive weight."

    # Calculate daily water intake target
    daily_target = calculate_daily_intake(gender, age, weight)

    # Open the users file and load data
    try:
        user_data = load_user_data()
        user_id = len(user_data['users']) + 1  # Auto-increment user ID

        # Create the new user record
        new_user = {
            "id": user_id,
            "username": username,
            "phone_number": phone_number,
            "gender": gender,
            "age": age,
            "weight": weight,
            "daily_target": daily_target,
            "water_intake": 0.0  # Initial water intake is 0
        }

        # Append the new user to the user data
        user_data['users'].append(new_user)

        # Save updated user data
        save_user_data(user_data)

        return f"Welcome, {username}! Your daily water intake target is {daily_target:.2f} liters."

    except OSError as os_error:
        return f"File system error occurred: {str(os_error)}"
    except json.JSONDecodeError:
        return "Error: Failed to decode user data file. Please check the file format."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def get_user_info(username):
    """
    Retrieve information about a specific user.
    Args:
        username (str): The username of the user to fetch information for.
    Returns:
        dict or str: The user's data if found, or a message indicating the user is not found.
    """
    if not username:
        return "Error: Username must be provided."

    user_data = load_user_data()

    for user in user_data['users']:
        if user['username'] == username:
            return user  # Return the user's data

    return "User not found."


def remove_user(username):
    """
    Remove a user from the system.
    Args:
        username (str): The username of the user to remove.
    Returns:
        str: A message indicating success or the error encountered.
    """
    if not username:
        return "Error: Username must be provided."

    user_data = load_user_data()

    # Check if the user exists in the system
    user_found = False
    for user in user_data['users']:
        if user['username'] == username:
            user_data['users'].remove(user)
            user_found = True
            break

    if not user_found:
        return "User not found."

    # Save updated user data
    save_user_data(user_data)
    return "User removed successfully!"
