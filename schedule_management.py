
from user_management import load_user_data, save_user_data
from fetch_data import get_random_quote
from sms_service import send_sms  # Import the real send_sms function
import schedule

# Notification limit and interval
NOTIFICATION_LIMIT = 3
NOTIFICATION_INTERVAL_MINUTES = 1


def send_reminder(username):
    """
    Send a reminder to the user with a motivational message and water intake suggestion.

    Args:
        username (str): The user's name.
    """
    user_data = load_user_data()
    users = user_data.get('users', [])  # Access 'users' key to get the list of users

    user = next((u for u in users if u['username'] == username), None)

    if not user:
        print(f"User '{username}' not found.")
        return

    reminders_sent = user.get("reminders_sent", 0)

    if reminders_sent >= NOTIFICATION_LIMIT:
        print(f"Max reminders sent for '{username}'.")
        return

    # Fetch daily water target from user_data.json
    daily_target = user.get("daily_target", 0)  # Assume this is in liters
    if daily_target <= 0:
        print(f"No valid daily water target found for '{username}'.")
        return

    # Calculate water intake per reminder
    water_per_notification = round(daily_target / NOTIFICATION_LIMIT, 2)

    # Fetch a motivational quote
    motivational_message = get_random_quote(max_length=100)
    if isinstance(motivational_message, dict):  # Handle API errors
        motivational_message = "Stay hydrated! Health is wealth."

    # Construct the reminder message
    reminder_message = (
        f"{motivational_message} Don't forget to drink {water_per_notification}l."
    )

    # Get user phone number
    phone_number = user.get("phone_number", "Unknown Number")

    # Send the SMS using sms_service.py
    response = send_sms(phone_number, reminder_message)
    if response.get("status") == "Error":
        print(f"Failed to send SMS to {username}: {response.get('description')}")
    else:
        print(f"SMS successfully sent to {username}: {reminder_message}")


def handle_user_response(username, message):
    """
    Handles the user's response to the reminder, either 'done' or 'skip'.
    If 'done', the user is considered to have completed the reminder.
    If 'skip', the reminder is skipped, and the next one is scheduled.

    Args:
        username (str): The user's name.
        message (str): The response from the user ("done" or "skip").
    """
    # Load user data from storage (assuming it's a JSON or similar structure)
    user_data = load_user_data()  # Load user data (this is assumed to be a function already implemented)
    users = user_data.get('users', [])

    # Find the user based on the username
    user = next((u for u in users if u['username'] == username), None)

    if not user:
        print(f"User '{username}' not found.")
        return

    if message.strip().lower() not in ['done', 'skip']:
        print("Invalid response. Please reply with 'done' or 'skip'.")
        return

    # Calculate water intake per reminder
    daily_target = user.get("daily_target", 0)  # Assume this is in liters
    reminders_sent = user.get("reminders_sent", 0)
    water_per_notification = round(daily_target / NOTIFICATION_LIMIT, 2)

    # Process user response and update state
    if message.strip().lower() == 'done':

        # Update the water intake if user answers 'done'
        user["water_intake"] = user.get("water_intake", 0) + water_per_notification
        print(f"User {username}'s water intake updated to {user['water_intake']:.2f} liters.")

    else:
        print(f"User {username} skipped the reminder.")

    # Increment reminders_sent count when user responds
    user["reminders_sent"] = reminders_sent + 1

    # Save user data after update
    save_user_data(user_data)

    # Check if user has completed all reminders
    if user["reminders_sent"] >= NOTIFICATION_LIMIT:
        print(f"User {username} has completed all reminders.")
        return  # Exit after completing all reminders

    # Schedule next reminder if the user has not responded to all reminders
    send_reminder(username)


def send_daily_statistics(username):
    """
    Send daily statistics to the user summarizing their water intake.
    """
    user_data = load_user_data()
    users = user_data.get('users', [])

    user = next((u for u in users if u['username'] == username), None)

    if not user:
        print(f"User '{username}' not found.")
        return

    water_intake = round(user.get("water_intake", 0), 2)  # Round the value to avoid floating-point issues
    daily_target = user.get("daily_target", 0)

    # Calculate percentage of daily target reached
    percentage = (water_intake / daily_target) * 100

    # Determine the message based on the percentage
    if percentage < 50:
        message = f"You're doing great, but could drink more. Stay hydrated tomorrow! You drank {water_intake}l out of {daily_target}l today."
    elif 50 <= percentage < 80:
        message = f"Good job! You're on the right track, but there's room for improvement. Keep it up! You drank {water_intake}l out of {daily_target}l today."
    elif percentage >= 95:
        message = f"Awesome! You hit your water goal today. Keep it up, you're doing amazing! You drank {water_intake}l out of {daily_target}l today."

    # Get user phone number
    phone_number = user.get("phone_number", "Unknown Number")

    # Send the message to the user
    send_sms(phone_number, message)
    print(f"Daily statistics sent to {username}: {message}")


def schedule_reminders():
    """
    Schedule reminders for all users at 1-2 minute intervals.
    """
    user_data = load_user_data()
    users = user_data.get('users', [])  # Access 'users' key to get the list of users

    for user in users:
        username = user['username']
        # Schedule reminders at 1-2 minute intervals
        schedule.every(NOTIFICATION_INTERVAL_MINUTES).minutes.do(send_reminder, username=username)


def schedule_daily_statistics_reminders():
    """
    Schedule daily statistics messages for all users at a set time.
    """
    user_data = load_user_data()
    users = user_data.get('users', [])  # Access 'users' key to get the list of users

    for user in users:
        username = user['username']
        water_intake = user.get("water_intake", 0)  # Ensure this is being updated properly
        daily_target = user.get("daily_target", 0)

        # Schedule daily statistics at 8 PM
        schedule.every().day.at("20:00").do(send_daily_statistics, username=username,
                                            water_intake=water_intake,
                                            daily_target=daily_target)
