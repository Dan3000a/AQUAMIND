import requests

# Define the URL and output file name
REQUESTING_URL = 'http://hackathons.masterschool.com:3030/team/registerNumber'
OUTPUT_FILE_NAME = "2_outputRegNum.html"

# Function to save text content to a file
def save_to_file(text, filename):
    with open(filename, "w") as fileobj:
        fileobj.write(text)

# Main function to handle user input, POST request, and saving the response
def main():
    # Prompt the user for input
    team_name = input("Enter the team name: ")
    phone_number = input("Enter the phone number (with country code, no +): ")

    # Validate phone number input
    if not phone_number.isdigit():
        print("Invalid phone number. Please enter only numeric characters.")
        return

    # Prepare the data to send
    data = {
        "phoneNumber": int(phone_number),
        "teamName": team_name
    }

    try:
        # Send a POST request with the data as JSON
        res = requests.post(REQUESTING_URL, json=data)

        # Check if the request was successful
        if res.status_code == 200:
            save_to_file(res.text, OUTPUT_FILE_NAME)
            print(f"Successfully registered phone number to team '{team_name}'.")
            print(f"Response saved to {OUTPUT_FILE_NAME}")
        else:
            print(f"Failed to register phone number. Status Code: {res.status_code}")
            print(f"Response: {res.text}")
    except requests.exceptions.RequestException as e:
        # Handle exceptions like connectivity issues
        print(f"An error occurred: {e}")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()