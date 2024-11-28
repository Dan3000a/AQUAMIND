import time

import IPython

from user_management import register_user
from schedule_management import schedule_reminders, send_reminder, handle_user_response, schedule_daily_statistics_reminders, send_daily_statistics
import schedule
from sms_service import send_sms, get_messages
TEAM_NAME = "WaterProof"

def get_all_numbers(messages_response):
    phone_numbers = set()
    for phone_messages in messages_response:
        if phone_messages != "491736536574":
            phone_numbers.update(phone_messages.keys())
    return list(phone_numbers)

def subscribe_reminders(numbers, message="Don't forget to drink water!", repeat=3, interval=60):
    for _ in range(repeat):
        for number in numbers:
            #send_sms(number, message)
            print(f"sent remainder to {number}")
        time.sleep(interval)

def get_last_message(phone_number, messages_response):
    for phone_messages in messages_response:
        if phone_number in phone_messages:
            messages = phone_messages[phone_number]
            messages.sort(key=lambda msg: msg['receivedAt'], reverse=True)
            return messages[0]['text']
    print("got No messages")
    return None

def send_sms_real(phone_number, message):
    """
    Sends an SMS via the SMS service.
    """
    response = send_sms(phone_number, message)
    if response.get("status") == "Success":
        print(f"SMS sent to {phone_number}: {message}")
    else:
        print(f"Failed to send SMS to {phone_number}: {response.get('description')}")

def fetch_user_response(phone_number, team_name, timeout=60, poll_interval=10):
    """
    Polls for user responses within a timeout period.
    """
    elapsed_time = 0
    while elapsed_time < timeout:
        messages_response = get_messages(team_name)  # Fetch messages for the team

        # Print the response to understand its structure
        print("Received messages_response:", messages_response)

        if isinstance(messages_response, list):  # Check if it's a list
            for message_group in messages_response:
                # Each group is a dictionary where the key is the phone number
                for phone, messages in message_group.items():
                    if phone == phone_number:
                        return messages[-1]
                        # for message in messages:
                        #     return message.get("text", "").strip().lower()
        else:
            print("Error: Expected a list of messages, but got:", type(messages_response))

        time.sleep(poll_interval)
        elapsed_time += poll_interval
    return "skip"  # Default response if no reply is received within the timeout

def parse_data(phone_number, message):
    """
    Processes the registration message from the user and adds them to the system.
    """
    user_details = message.split()
    if len(user_details) != 4:
        raise ValueError("Incorrect input format.")

    username, age, weight, gender = user_details
    if not age.isdigit() or not weight.replace('.', '', 1).isdigit():
        raise ValueError("Age must be an integer and weight a float.")

    age = int(age)
    weight = float(weight)
    gender = gender.lower()
    if gender not in ['male', 'female']:
        raise ValueError("Gender must be 'male' or 'female'.")

    return username, age, weight, gender
    #     # Register the user
    #     result_message = register_user(username, phone_number, gender, age, weight)
    #     send_sms_real(phone_number, result_message)
    #
    #     if "Welcome" in result_message:
    #         # Now, schedule reminders and daily statistics
    #         schedule_reminders()
    #         schedule_daily_statistics_reminders()
    #
    #         # Send the first reminder immediately
    #         send_reminder(username)
    #
    # except ValueError as e:
    #     send_sms_real(phone_number, f"Invalid input: {e}. Please try again.")

def handle_incoming_message(phone_number, message):
    """
    Handles incoming SMS messages and processes user data input for registration.
    """
    process_registration(phone_number, message)  # Register the user

def send_get_data_sms(phone_number):
    message = (
        "Please send your username, age, weight, gender (e.g., john_doe 30 70 male)"
    )
    sender = ""
    send_sms(phone_number, message, sender)

def main():
    """
# 1. fetch all messages we have so far
    for each number:
        # 2. users get's an SMS for data
            # using the send_sms function
        # 3. Program saves user data
            #  user_management module
            # 4. program calculates hydration stuff
                #using the hydration logic
        # 5. user gets a remainder + quote every minute
            # using the send remainder functino from the schedule management.
        # 6. at the end of the day send statistics summary
    # using the schuedule management module
    Handles SMS-based user interaction.
    """
    print("Starting AquaMind SMS Service...")


    # phone_number = input("Enter phone number: ").strip()
    # team_name = "WaterProof"  # Set your team name here
    #
    # # Register the phone number with the team
    # subscribe_message = f"SUBSCRIBE {team_name}"
    # send_sms_real(phone_number, subscribe_message)  # Send subscription message
    messages_dict = get_messages(TEAM_NAME)
    print("step 0 - get_messages ")
    numbers = get_all_numbers(messages_dict)
    print("step 1 - get_all_numbers ")

    for number in numbers:
        send_get_data_sms(number) # Functino that get's a phone number, and sends an SMS that asks for details.
        print("step 2 - send_get_data_sms ")
        data = get_last_message(number, messages_dict)
        print("step 3 - get_last_message ")
        username, age, weight, gender = parse_data(number, data)
        print("step 4 - parse_data ")
        result_message = register_user(username, number, gender, age, weight)
        print("step 5 - register_user ")

    subscribe_reminders(numbers)
    print("step 6 - subscribe_reminders ")

    # # Wait for the user's response via SMS
    # print("Waiting for user registration details via SMS...")
    # message = fetch_user_response(phone_number, team_name, timeout=120)  # 2-minute timeout for response
    #
    # if message.lower() == "exit":
    #     print("Exiting.")
    #     return
    #
    # # Process the registration and send the first reminder
    # handle_incoming_message(phone_number, message)
    #
    # # Loop for 3 reminders and process user responses
    # for _ in range(3):  # 3 reminders
    #     username = message.split()[0]  # Extract username for reminder
    #     send_reminder(username)  # Send reminder SMS
    #     user_response = fetch_user_response(phone_number, team_name)  # Poll for response
    #     handle_user_response(username, user_response)  # Process the response
    #
    #     # Run scheduled tasks in the background (non-blocking)
    #     schedule.run_pending()
    #     time.sleep(1)
    #
    # # Fetch user information to send statistics
    # username = message.split()[0]
    # send_daily_statistics(username)  # Send daily statistics once


if __name__ == "__main__":
    main()
