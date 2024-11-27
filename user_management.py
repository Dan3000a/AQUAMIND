import json
import os

# Constants for file paths and modes
USER_DATA_FILE_PATH = "user_data.json"
READ_MODE = "r"
WRITE_MODE = "w"


def load_user_data():
    """Load user data from the JSON file."""
    if not os.path.exists(USER_DATA_FILE_PATH):
        return {}
    try:
        with open(USER_DATA_FILE_PATH, READ_MODE) as user_file:
            return json.load(user_file)
    except json.JSONDecodeError:
        print("Error: Corrupted user data file.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return {}


def save_user_data(user_data):
    """Save the updated user data to the JSON file."""
    try:
        with open(USER_DATA_FILE_PATH, WRITE_MODE) as user_file:
            json.dump(user_data, user_file, indent=4)
    except IOError as io_error:
        print(f"File I/O error: {str(io_error)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def add_user(username, phone_number, age, weight, gender):
    """Add a new user to the system with additional details."""
    # Validate inputs
    if not username or not phone_number or not age or not weight or not gender:
        return "Error: All fields (username, phone number, age, weight, gender) must be provided."

    if not isinstance(age, int) or age <= 0:
        return "Error: Age must be a positive integer."

    if not isinstance(weight, (int, float)) or weight <= 0:
        return "Error: Weight must be a positive number."

    if gender.lower() not in ["male", "female", "other"]:
        return "Error: Gender must be 'Male', 'Female', or 'Other'."

    user_data = load_user_data()

    if username in user_data:
        return "User already exists."

    user_data[username] = {
        "phone_number": phone_number,
        "age": age,
        "weight": weight,
        "gender": gender.capitalize()
    }
    save_user_data(user_data)
    return "User added successfully!"


def remove_user(username):
    """Remove a user from the system."""
    if not username:
        return "Error: Username must be provided."

    user_data = load_user_data()

    if username not in user_data:
        return "User not found."

    del user_data[username]
    save_user_data(user_data)
    return "User removed successfully!"


def get_user_info(username):
    """Retrieve information about a specific user."""
    if not username:
        return "Error: Username must be provided."

    user_data = load_user_data()

    if username in user_data:
        return user_data[username]
    return "User not found."


def list_all_users():
    """List all users in the system."""
    return load_user_data()
