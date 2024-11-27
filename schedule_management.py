import schedule
import time
from datetime import datetime
from user_management import load_user_data, save_user_data
from fetch_data import get_random_quote
from sms_service import send_sms  # Import the real send_sms function

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

    if username not in user_data:
        print(f"User '{username}' not found.")
        return

    user = user_data[username]
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
    motivational_message = get_random_quote(max_length=150)
    if isinstance(motivational_message, dict):  # Handle API errors
        motivational_message = "Stay hydrated! Health is wealth."

    # Construct the reminder message
    reminder_message = (
        f"{motivational_message} Don't forget to drink {water_per_notification} l."
    )

    # Get user phone number
    phone_number = user.get("phoneNumber", "Unknown Number")

    # Send the SMS using sms_service.py
    response = send_sms(phone_number, reminder_message)
    if response.get("status") == "Error":
        print(f"Failed to send SMS to {username}: {response.get('description')}")
    else:
        print(f"SMS successfully sent to {username}: {reminder_message}")

    # Update reminder count
    user["reminders_sent"] = reminders_sent + 1
    save_user_data(user_data)


def schedule_reminders():
    """
    Schedule reminders for all users at 1-2 minute intervals.
    """
    user_data = load_user_data()

    for username in user_data.keys():
        # Schedule reminders at 1-2 minute intervals
        schedule.every(NOTIFICATION_INTERVAL_MINUTES).minutes.do(send_reminder, username=username)


if __name__ == "__main__":
    # Initialize reminders_sent to 0 for all users
    user_data = load_user_data()
    for user in user_data.values():
        user["reminders_sent"] = 0
    save_user_data(user_data)

    print("Starting AquaMind Reminder Scheduler...")
    schedule_reminders()

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
