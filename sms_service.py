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


# API Functions
def add_new_team(team_name):
    """
    Adds a new team by sending a POST request to the API.
    Args:
        team_name (str): Name of the team to be created.
    Returns:
        dict: JSON response from the API or an error message.
    """
    url = f"{BASE_URL}/team/addNewTeam"
    data = {"teamName": team_name}  # Team name to be sent in the request.

    try:
        res = requests.post(url, json=data)  # Send the POST request.
        print(f"Raw Response Text: {res.text}")  # Log raw response for debugging.
        if res.status_code == 200:  # Check if the request was successful.
            try:
                response_json = res.json()  # Parse JSON response.
                save_to_file(response_json, "1_TeamAdded.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:  # Handle invalid JSON response.
                save_to_file({"error": res.text}, "1_TeamAdded.html")
                return {"error": "Invalid JSON response"}
        elif res.status_code == 500 and "already exists" in res.text:
            # Handle team-name conflict.
            print(f"Error: Team '{team_name}' already exists.")
            return {"error": f"Team '{team_name}' already exists."}
        else:
            save_to_file({"error": res.text}, "1_TeamAdded.html")  # Save any other errors.
            return {"error": res.text}
    except requests.RequestException as e:  # Handle network issues.
        print(f"Request failed: {e}")
        return {"error": str(e)}


def register_number(phone_number, team_name):
    """
    Registers a phone number to a specific team.
    Args:
        phone_number (str): The phone number to register.
        team_name (str): The team name to associate the number with.
    Returns:
        dict: JSON response from the API or an error message.
    """
    phone_number = phone_number.lstrip("+")  # Remove '+' if present.
    if not phone_number.isdigit():  # Validate a phone number format.
        print("Error: Phone number must contain only digits.")
        return {"status": "Error", "description": "Invalid phone number format."}
    if not phone_number.startswith("49"):  # Ensure it starts with the German country code.
        print("Error: Phone number must start with country code '49'.")
        return {"status": "Error", "description": "Phone number must start with country code 49."}

    url = f"{BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": team_name}  # Request payload.

    try:
        res = requests.post(url, json=data)  # Send the POST request.
        print(f"Raw Response Text: {res.text}")  # Log raw response for debugging.
        if res.status_code == 200:  # Check if the request was successful.
            try:
                response_json = res.json()
                save_to_file(response_json, "2_outputRegNum.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:  # Handle invalid JSON response.
                save_to_file({"error": res.text}, "2_outputRegNum.html")
                return {"error": "Invalid JSON response"}
        else:
            save_to_file({"error": res.text}, "2_outputRegNum.html")  # Save any other errors.
            return {"error": res.text}
    except requests.RequestException as e:  # Handle network issues.
        print(f"Request failed: {e}")
        return {"error": str(e)}


def get_messages(team_name):
    """
    Retrieves all messages for a specific team.
    Args:
        team_name (str): The team name to fetch messages for.
    Returns:
        dict: JSON response from the API or an error message.
    """
    url = f"{BASE_URL}/team/getMessages/{team_name}"  # API endpoint.
    try:
        res = requests.get(url)  # Send the GET request.
        print(f"Raw Response Text: {res.text}")  # Log raw response for debugging.
        if res.status_code == 200:  # Check if the request was successful.
            try:
                response_json = res.json()
                save_to_file(response_json, "3_outputMessages.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:  # Handle invalid JSON response.
                save_to_file({"error": res.text}, "3_outputMessages.html")
                return {"error": "Invalid JSON response"}
        else:
            save_to_file({"error": res.text}, "3_outputMessages.html")  # Save any other errors.
            return {"error": res.text}
    except requests.RequestException as e:  # Handle network issues.
        print(f"Request failed: {e}")
        return {"error": str(e)}


def send_sms(phone_number, message, sender=""):
    """
    Sends an SMS message to a specified phone number.
    Args:
        phone_number (str): The recipient's phone number.
        message (str): The SMS content.
        sender (str): The sender ID (optional).
    Returns:
        dict: JSON response from the API or an error message.
    """
    if len(message) > 160:  # Validate message length.
        print(f"Error: Message exceeds 160 characters ({len(message)}).")
        return {"status": "Error", "description": "Message length exceeds limit."}

    phone_number = phone_number.lstrip("+")  # Remove '+' if present.
    if not phone_number.isdigit() or not phone_number.startswith("49"):  # Validate the phone number format.
        print("Error: Invalid phone number format.")
        return {"status": "Error", "description": "Invalid phone number format."}

    url = f"{BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": sender}  # Request payload.

    try:
        res = requests.post(url, json=data)  # Send the POST request.
        print(f"Raw Response Text: {res.text}")  # Log raw response for debugging.
        if res.status_code == 200:  # Check if the request was successful.
            try:
                response_json = res.json()
                save_to_file(response_json, "4_outputSendSMS.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:  # Handle invalid JSON response.
                save_to_file({"error": res.text}, "4_outputSendSMS.html")
                return {"error": "Invalid JSON response"}
        else:
            save_to_file({"error": res.text}, "4_outputSendSMS.html")  # Save any other errors.
            return {"error": res.text}
    except requests.RequestException as e:  # Handle network issues.
        print(f"Request failed: {e}")
        return {"error": str(e)}


# Interactive Menu
def main():
    """
    Provides a menu-driven interface for interacting with the SMS service.
    """
    print("Welcome to the SMS Service!")
    while True:
        print("\nSelect an option:")
        print("1. Add a New Team")
        print("2. Register a Phone Number")
        print("3. Retrieve Messages")
        print("4. Send SMS")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            team_name = input("Enter team name: ")
            response = add_new_team(team_name)
            if "already exists" in response.get("error", ""):
                print("Please choose a different team name.")
            print("Response:", response)
        elif choice == "2":
            phone_number = input("Enter phone number (e.g., +49123456789): ")
            team_name = input("Enter team name: ")
            response = register_number(phone_number, team_name)
            print("Response:", response)
        elif choice == "3":
            team_name = input("Enter team name: ")
            response = get_messages(team_name)
            print("Messages:", response)
        elif choice == "4":
            phone_number = input("Enter phone number (e.g., +49123456789): ")
            message = input("Enter message: ")
            sender = input("Enter sender (or leave blank): ")
            response = send_sms(phone_number, message, sender)
            print("Response:", response)
        elif choice == "5":
            print("Exiting SMS Service...")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the script
if __name__ == "__main__":
    main()
