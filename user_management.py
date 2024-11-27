import json
import os

# Constants for file paths and modes
USER_DATA_FILE_PATH = "user_data.json"
FILE_READ_MODE = "r"
FILE_WRITE_MODE = "w"

def load_user_data():
    """
    Load user data from the JSON file.
    
    Returns:
        dict: A dictionary containing user data. Returns an empty dictionary if the file doesn't exist.
    """
    if not os.path.exists(USER_DATA_FILE_PATH):
        return {}
    
    with open(USER_DATA_FILE_PATH, FILE_READ_MODE) as user_file:
        return json.load(user_file)

def save_user_data(user_data):
    """
    Save the updated user data to the JSON file.
    
    Args:
        user_data (dict): The dictionary containing user data to be saved.
    """
    with open(USER_DATA_FILE_PATH, FILE_WRITE_MODE) as user_file:
        json.dump(user_data, user_file, indent=4)

def add_user(username, phone_number, age, weight, gender):
    """
    Add a new user to the system with additional details.
    
    Args:
        username (str): The user's name.
        phone_number (str): The user's phone number.
        age (int): The user's age.
        weight (float): The user's weight in kilograms.
        gender (str): The user's gender.
    
    Returns:
        str: Confirmation message indicating success or failure.
    """
    user_data = load_user_data()
    
    if username in user_data:
        return "User already exists."

    user_data[username] = {
        "phoneNumber": phone_number,
        "age": age,
        "weight": weight,
        "gender": gender
    }
    save_user_data(user_data)
    return "User added successfully!"

def remove_user(username):
    """
    Remove a user from the system.
    
    Args:
        username (str): The user's name to be removed.
    
    Returns:
        str: Confirmation message indicating success or failure.
    """
    user_data = load_user_data()
    
    if username not in user_data:
        return "User not found."

    del user_data[username]
    save_user_data(user_data)
    return "User removed successfully!"

def get_user_info(username):
    """
    Retrieve information about a specific user.
    
    Args:
        username (str): The user's name to retrieve information for.
    
    Returns:
        dict or str: User information dictionary or an error message if the user is not found.
    """
    user_data = load_user_data()
    
    if username in user_data:
        return user_data[username]
    return "User not found."

def list_all_users():
    """
    List all users in the system.
    
    Returns:
        dict: A dictionary containing all user information.
    """
    return load_user_data()
