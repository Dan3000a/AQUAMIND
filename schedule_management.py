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
        f"{motivational_message} Don't forget to drink approximately {water_per_notification} liters of water."
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


def send_daily_statistics(username, water_intake, daily_target):
    """
    Send daily statistics to the user summarizing their water intake.

    Args:
        username (str): The user's name.
        water_intake (float): The total water intake for the day in liters.
        daily_target (float): The user's daily water intake target in liters.
    """
    # Calculate percentage of daily target reached
    percentage = (water_intake / daily_target) * 100

    # Determine the message based on the percentage
    if percentage < 50:
        message = "You're doing great, but could drink more. Stay hydrated tomorrow!"
    elif 50 <= percentage < 80:
        message = "Good job! You're on the right track, but there's room for improvement. Keep it up!"
    elif percentage >= 100:
        message = "Awesome! You hit your water goal today. Keep it up, you're doing amazing!"
    else:
        message = "Great job! You're doing well, but there's always room to improve!"

    # Get user phone number
    phone_number = load_user_data().get(username, {}).get("phoneNumber", "Unknown Number")

    # Send the message to the user
    send_sms(phone_number, message)
    print(f"Daily statistics sent to {username}: {message}")


def schedule_reminders():
    """
    Schedule reminders for all users at 1-2 minute intervals.
    """
    user_data = load_user_data()

    for username in user_data.keys():
        # Schedule reminders at 1-2 minute intervals
        schedule.every(NOTIFICATION_INTERVAL_MINUTES).minutes.do(send_reminder, username=username)


def schedule_daily_statistics_reminders():
    """
    Schedule daily statistics messages for all users at a set time.
    """
    user_data = load_user_data()

    for username, user in user_data.items():
        water_intake = user.get("water_intake", 0)  # Ensure this is being updated properly
        daily_target = user.get("daily_target", 0)

        # Schedule daily statistics at 8 PM
        schedule.every().day.at("20:00").do(send_daily_statistics, username=username,
                                            water_intake=water_intake,
                                            daily_target=daily_target)


if __name__ == "__main__":
    # Initialize reminders_sent to 0 for all users
    user_data = load_user_data()
    for user in user_data.values():
        user["reminders_sent"] = 0
    save_user_data(user_data)

    print("Starting AquaMind Reminder Scheduler...")
    schedule_reminders()
    schedule_daily_statistics_reminders()

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
