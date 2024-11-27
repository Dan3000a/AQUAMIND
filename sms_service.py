
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
    # Validate team name
    team_name = team_name.strip()
    if not team_name or not team_name.isalpha():
        print("Error: Team name must contain only letters and cannot be blank.")
        return {"status": "Error", "description": "Invalid team name."}

    url = f"{BASE_URL}/team/addNewTeam"
    data = {"teamName": team_name}  # Prepare the request payload.

    try:
        res = requests.post(url, json=data)  # Send the POST request.
        print(f"Raw Response Text: {res.text}")  # Log the raw response.

        if res.status_code == 200:  # Check if the request was successful.
            try:
                response_json = res.json()  # Parse the response as JSON.
                save_to_file(response_json, "1_TeamAdded.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:
                save_to_file({"error": res.text}, "1_TeamAdded.html")  # Handle invalid JSON.
                return {"error": "Invalid JSON response"}
        elif res.status_code == 500 and "already exists" in res.text:
            print(f"Error: Team '{team_name}' already exists.")
            return {"error": f"Team '{team_name}' already exists."}
        else:
            save_to_file({"error": res.text}, "1_TeamAdded.html")
            return {"error": res.text}
    except requests.RequestException as e:
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
    phone_number = phone_number.strip().lstrip("+")  # Remove '+' and spaces.

    # Validate phone number format
    if not phone_number.isdigit():
        print("Error: Phone number must only contain digits.")
        return {"status": "Error", "description": "Invalid phone number format."}
    if not phone_number.startswith("49"):
        print("Error: Phone number must start with country code '49'.")
        return {"status": "Error", "description": "Phone number must start with country code 49."}

    url = f"{BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": team_name}  # Request payload.

    try:
        res = requests.post(url, json=data)  # Send the POST request.
        print(f"Raw Response Text: {res.text}")  # Log the raw response.

        if res.status_code == 200:
            try:
                response_json = res.json()  # Parse the response as JSON.
                save_to_file(response_json, "2_outputRegNum.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:
                save_to_file({"error": res.text}, "2_outputRegNum.html")  # Handle invalid JSON.
                return {"error": "Invalid JSON response"}
        else:
            save_to_file({"error": res.text}, "2_outputRegNum.html")
            return {"error": res.text}
    except requests.RequestException as e:
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
        print(f"Raw Response Text: {res.text}")  # Log the raw response.

        if res.status_code == 200:
            try:
                response_json = res.json()  # Parse the response as JSON.
                save_to_file(response_json, "3_outputMessages.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:
                save_to_file({"error": res.text}, "3_outputMessages.html")  # Handle invalid JSON.
                return {"error": "Invalid JSON response"}
        else:
            save_to_file({"error": res.text}, "3_outputMessages.html")
            return {"error": res.text}
    except requests.RequestException as e:
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
    if len(message) > 160:
        print(f"Error: Message exceeds 160 characters ({len(message)}).")
        return {"status": "Error", "description": "Message length exceeds limit."}

    phone_number = phone_number.strip().lstrip("+")  # Remove '+' and spaces.
    if not phone_number.isdigit() or not phone_number.startswith("49"):
        print("Error: Invalid phone number format.")
        return {"status": "Error", "description": "Invalid phone number format."}

    url = f"{BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": sender}  # Request payload.

    try:
        res = requests.post(url, json=data)  # Send the POST request.
        print(f"Raw Response Text: {res.text}")  # Log the raw response.

        if res.status_code == 200:
            try:
                response_json = res.json()  # Parse the response as JSON.
                save_to_file(response_json, "4_outputSendSMS.html")  # Save response to file.
                return response_json
            except json.JSONDecodeError:
                save_to_file({"error": res.text}, "4_outputSendSMS.html")  # Handle invalid JSON.
                return {"error": "Invalid JSON response"}
        else:
            save_to_file({"error": res.text}, "4_outputSendSMS.html")
            return {"error": res.text}
    except requests.RequestException as e:
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
            print("Exiting SMS Service...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Run the script
if __name__ == "__main__":
    main()