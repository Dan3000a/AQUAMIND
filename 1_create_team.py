import requests

# Define the URL and output file name
REQUESTING_URL = 'http://hackathons.masterschool.com:3030/team/addNewTeam'
OUTPUT_FILE_NAME = "1_TeamAdded.html"

# Data to send in the POST request
data = {
    "teamName": "WaterProof"
}

# Function to save text content to a file
def save_to_file(text, filename):
    with open(filename, "w") as fileobj:
        fileobj.write(text)

# Main function to handle the POST request and saving the response
def main():
    try:
        # Send a POST request with the data as JSON
        res = requests.post(REQUESTING_URL, json=data)

        # Check if the request was successful
        if res.status_code == 200:
            save_to_file(res.text, OUTPUT_FILE_NAME)
            print(f"Successfully saved response to {OUTPUT_FILE_NAME}")
        else:
            print(f"Failed to create team. Status Code: {res.status_code}")
            print(f"Response: {res.text}")
    except requests.exceptions.RequestException as e:
        # Handle exceptions like connectivity issues
        print(f"An error occurred: {e}")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()