import requests
import json

# Base API URL
BASE_URL = 'http://hackathons.masterschool.com:3030'

# Utility Functions
def save_to_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# API Functions
def add_new_team(team_name):
    url = f"{BASE_URL}/team/addNewTeam"
    data = {"teamName": team_name}

    try:
        res = requests.post(url, json=data)

        # Log raw response for debugging
        print(f"Raw Response Text: {res.text}")

        if res.status_code == 200:
            # Handle plain text response
            if res.headers.get("Content-Type") == "text/plain":
                save_to_file({"message": res.text}, "1_TeamAdded.html")
                return {"message": res.text}
            try:
                response_json = res.json()
                save_to_file(response_json, "1_TeamAdded.html")
                return response_json
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON.")
                save_to_file({"error": res.text}, "1_TeamAdded.html")
                return {"error": "Invalid JSON response"}
        elif res.status_code == 500 and "already exists" in res.text:
            print(f"Error: Team '{team_name}' already exists. Please choose a new name.")
            return {"error": f"Team '{team_name}' already exists."}
        else:
            print(f"Error: Received status code {res.status_code}. Response: {res.text}")
            save_to_file({"error": res.text}, "1_TeamAdded.html")
            return {"error": res.text}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}

def register_number(phone_number, team_name):
    if phone_number.startswith("+"):
        phone_number = phone_number[1:]  # Remove '+'

    if not phone_number.isdigit():
        print("Error: Phone number must only contain digits (and no '+').")
        return {"status": "Error", "description": "Invalid phone number format."}

    if not phone_number.startswith("49"):
        print("Error: Phone number must begin with the German country code '49'.")
        return {"status": "Error", "description": "Phone number must start with country code 49."}

    url = f"{BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": team_name}

    try:
        res = requests.post(url, json=data)

        # Log raw response for debugging
        print(f"Raw Response Text: {res.text}")

        if res.status_code == 200:
            # Handle plain text response
            if res.headers.get("Content-Type") == "text/plain":
                save_to_file({"message": res.text}, "2_outputRegNum.html")
                return {"message": res.text}
            try:
                response_json = res.json()
                save_to_file(response_json, "2_outputRegNum.html")
                return response_json
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON.")
                save_to_file({"error": res.text}, "2_outputRegNum.html")
                return {"error": "Invalid JSON response"}
        else:
            print(f"Error: Received status code {res.status_code}. Response: {res.text}")
            save_to_file({"error": res.text}, "2_outputRegNum.html")
            return {"error": res.text}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}

def get_messages(team_name):
    url = f"{BASE_URL}/team/getMessages/{team_name}"
    try:
        res = requests.get(url)

        # Log raw response for debugging
        print(f"Raw Response Text: {res.text}")

        if res.status_code == 200:
            try:
                response_json = res.json()
                save_to_file(response_json, "3_outputMessages.html")
                return response_json
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON.")
                save_to_file({"error": res.text}, "3_outputMessages.html")
                return {"error": "Invalid JSON response"}
        else:
            print(f"Error: Received status code {res.status_code}. Response: {res.text}")
            save_to_file({"error": res.text}, "3_outputMessages.html")
            return {"error": res.text}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}

def send_sms(phone_number, message, sender=""):
    if len(message) > 160:
        print(f"Error: Message exceeds 160 characters ({len(message)}).")
        return {"status": "Error", "description": "Message length exceeds limit."}

    if not phone_number.isdigit() or not phone_number.startswith("49"):
        print("Error: Invalid phone number format.")
        return {"status": "Error", "description": "Invalid phone number format."}

    url = f"{BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": sender}

    try:
        res = requests.post(url, json=data)

        # Log raw response for debugging
        print(f"Raw Response Text: {res.text}")

        if res.status_code == 200:
            try:
                response_json = res.json()
                save_to_file(response_json, "4_outputSendSMS.html")
                return response_json
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON.")
                save_to_file({"error": res.text}, "4_outputSendSMS.html")
                return {"error": "Invalid JSON response"}
        else:
            print(f"Error: Received status code {res.status_code}. Response: {res.text}")
            save_to_file({"error": res.text}, "4_outputSendSMS.html")
            return {"error": res.text}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}

# Interactive Menu
def main():
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
            phone_number = input("Enter phone number (must start with country code, without '+'): ")
            team_name = input("Enter team name: ")
            response = register_number(phone_number, team_name)
            print("Response:", response)
        elif choice == "3":
            team_name = input("Enter team name: ")
            response = get_messages(team_name)
            print("Messages:", response)
        elif choice == "4":
            phone_number = input("Enter phone number (without +): ")
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