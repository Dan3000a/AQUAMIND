import requests
import json

# Base API URL
BASE_URL = 'http://hackathons.masterschool.com:3030'

# Save data to a JSON file
def save_to_file(data, filename):
    """
    Save data as JSON to a specified file.
    Args:
        data (dict): Data to save.
        filename (str): File name where data is saved.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Load user data from JSON
def load_user_data(filename="users.json"):
    """
    Load user data from the specified JSON file.
    Returns an empty dictionary if the file is not found.
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

# Save user data to JSON
def save_user_data(data, filename="users.json"):
    """
    Save user data to the specified JSON file.
    Args:
        data (dict): User data to save.
        filename (str): File name where data is saved.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Send SMS through the external API
def send_sms(phone_number, message, sender=""):
    """
    Send an SMS message to the given phone number.
    Args:
        phone_number (str): Recipient's phone number.
        message (str): The SMS content.
        sender (str): Sender name or ID (optional).
    Returns:
        dict: Response from the SMS API or an error message.
    """
    phone_number = phone_number.lstrip("+")  # Strip '+' if present
    if not phone_number.isdigit() or not phone_number.startswith("49"):  # Validate phone number
        return {"status": "Error", "description": "Invalid phone number format."}

    if len(message) > 160:  # Validate message length
        return {"status": "Error", "description": "Message exceeds 160 characters."}

    url = f"{BASE_URL}/sms/send"  # API endpoint
    data = {"phoneNumber": phone_number, "message": message, "sender": sender}  # Request payload

    try:
        res = requests.post(url, json=data)  # Send POST request
        if res.status_code == 200:  # Check success
            return res.json()
        else:
            return {"status": "Error", "description": res.text}
    except requests.RequestException as e:  # Handle connection errors
        return {"status": "Error", "description": str(e)}

# Process user responses ('done' or 'skip')
def process_user_response(phone_number, response):
    """
    Process a user's response to update their water intake.
    Args:
        phone_number (str): The user's phone number.
        response (str): The user response ('done' or 'skip').
    Returns:
        dict: Status of the processing.
    """
    user_data = load_user_data()  # Load user data
    user = next((u for u in user_data['users'] if u['phone_number'] == phone_number), None)  # Find user
    if not user:  # User not found
        return {"status": "Error", "description": "User not found."}

    if response.lower() == "done":  # Update water intake for 'done'
        user['water_intake'] += user['daily_target'] / 3  # Increment by one-third of daily target

    save_user_data(user_data)  # Save updated data
    return {"status": "Success", "description": "User response processed."}

# Standalone testing menu
if __name__ == "__main__":
    print("Welcome to the SMS Service!")
    while True:
        print("\nSelect an option:")
        print("1. Send SMS")
        print("2. Process User Response")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            phone_number = input("Enter phone number (e.g., +49123456789): ")
            message = input("Enter message: ")
            sender = input("Enter sender (or leave blank): ")
            response = send_sms(phone_number, message, sender)
            print("Response:", response)
        elif choice == "2":
            phone_number = input("Enter phone number (e.g., +49123456789): ")
            user_response = input("Enter user response ('done' or 'skip'): ")
            response = process_user_response(phone_number, user_response)
            print("Response:", response)
        elif choice == "3":
            print("Exiting SMS Service...")
            break
        else:
            print("Invalid choice. Please try again.")