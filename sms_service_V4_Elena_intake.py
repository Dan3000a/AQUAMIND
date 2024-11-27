import requests
import json

# Base API URL
BASE_URL = 'http://hackathons.masterschool.com:3030'

# Utility Functions
def save_to_file(data, filename):
    """
    Saves JSON data to a file.
    Args:
        data (dict): Data to be saved.
        filename (str): The name of the file.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# User Data Functions
def load_user_data():
    """
    Loads user data from a JSON file.
    Returns:
        dict: User data.
    """
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

def save_user_data(user_data):
    """
    Saves user data to a JSON file.
    Args:
        user_data (dict): User data to save.
    """
    with open("user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)

# New Function: Process User Response
def process_user_response(phone_number, response):
    """
    Process the user response (either 'done' or 'skip') to update their water intake.
    Args:
        phone_number (str): The user's phone number.
        response (str): The user response (either 'done' or 'skip').
    Returns:
        dict: A JSON response with the status.
    """
    user_data = load_user_data()
    # Find the user by phone number
    user = next((u for u in user_data['users'] if u['phone_number'] == phone_number), None)
    if not user:
        return {"status": "Error", "description": "User not found."}
    if response.lower() == "done":
        user['water_intake'] += user['daily_target'] / 3  # Increase water intake by 1/3 of the daily target
    elif response.lower() == "skip":
        pass  # No water intake is added if the user skips
    # Save updated user data
    save_user_data(user_data)
    return {"status": "Success", "description": "User response processed."}

# API Functions
# (Retain the existing API functions like add_new_team, register_number, get_messages, send_sms)

# Interactive Menu
def main():
    """
    Provides a menu-driven interface for interacting with the SMS service and user responses.
    """
    print("Welcome to the SMS and Water Intake Service!")
    while True:
        print("\nSelect an option:")
        print("1. Add a New Team")
        print("2. Register a Phone Number")
        print("3. Retrieve Messages")
        print("4. Send SMS")
        print("5. Process User Response (Water Intake)")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            team_name = input("Enter team name: ").strip()
            response = add_new_team(team_name)
            if "already exists" in response.get("error", ""):
                print("Please choose a different team name.")
            print("Response:", response)
        elif choice == "2":
            phone_number = input("Enter phone number (e.g., +49123456789): ").strip()
            team_name = input("Enter team name: ").strip()
            response = register_number(phone_number, team_name)
            print("Response:", response)
        elif choice == "3":
            team_name = input("Enter team name: ").strip()
            response = get_messages(team_name)
            print("Messages:", response)
        elif choice == "4":
            phone_number = input("Enter phone number (e.g., +49123456789): ").strip()
            message = input("Enter message: ").strip()
            sender = input("Enter sender (or leave blank): ").strip()
            response = send_sms(phone_number, message, sender)
            print("Response:", response)
        elif choice == "5":
            phone_number = input("Enter your phone number (e.g., +49123456789): ").strip()
            response_type = input("Enter your response ('done' or 'skip'): ").strip()
            response = process_user_response(phone_number, response_type)
            print("Response:", response)
        elif choice == "6":
            print("Exiting Service...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Run the script
if __name__ == "__main__":
    main()