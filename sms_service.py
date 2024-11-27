import requests
import json

# Base API URL
BASE_URL = 'http://hackathons.masterschool.com:3030'

# Utility Functions
def save_to_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)

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
    res = requests.post(url, json=data)
    save_to_file(res.json(), "1_TeamAdded.html")
    return res.json()

def register_number(phone_number, team_name):
    url = f"{BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": team_name}
    res = requests.post(url, json=data)
    save_to_file(res.json(), "2_outputRegNum.html")
    return res.json()

def get_messages(team_name):
    url = f"{BASE_URL}/team/getMessages/{team_name}"
    res = requests.get(url)
    save_to_file(res.json(), "3_outputMessages.html")
    return res.json()

def send_sms(phone_number, message, sender=""):
    url = f"{BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": sender}
    res = requests.post(url, json=data)
    save_to_file(res.json(), "4_outputSendSMS.html")
    return res.json()

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
            print("Response:", response)
        elif choice == "2":
            phone_number = input("Enter phone number (without +): ")
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