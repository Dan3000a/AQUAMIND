import requests

# Define the base URL and output file name
BASE_URL = 'http://hackathons.masterschool.com:3030/team/getMessages/'
OUTPUT_FILE_NAME = "3_outputMessages.html"

# Function to save text content to a file
def save_to_file(text, filename):
    with open(filename, "w") as fileobj:
        fileobj.write(text)

# Main function to handle the GET request and saving the response
def main():
    # Prompt the user for the team name
    team_name = input("Enter the team name: ")

    # Validate the team name
    if not team_name.strip():
        print("Invalid team name. Please provide a valid name.")
        return

    # Construct the request URL
    requesting_url = BASE_URL + team_name

    try:
        # Send a GET request
        res = requests.get(requesting_url)

        # Check if the request was successful
        if res.status_code == 200:
            save_to_file(res.text, OUTPUT_FILE_NAME)
            print(f"Messages for team '{team_name}' retrieved successfully.")
            print(f"Response saved to {OUTPUT_FILE_NAME}")
        else:
            print(f"Failed to retrieve messages. Status Code: {res.status_code}")
            print(f"Response: {res.text}")
    except requests.exceptions.RequestException as e:
        # Handle exceptions like connectivity issues
        print(f"An error occurred: {e}")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()