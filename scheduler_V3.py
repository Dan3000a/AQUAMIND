import schedule
import time
from fetch_data import get_random_quote
from sms_service import send_sms, load_user_data, save_user_data

# Constants for notification behavior
NOTIFICATION_LIMIT = 3  # Max reminders per user per day
NOTIFICATION_INTERVAL_MINUTES = 1  # Interval for sending reminders


def send_reminder(username):
    """
    Send a reminder SMS to the user with a motivational quote and water intake suggestion.
    Args:
        username (str): The username of the recipient.
    """
    user_data = load_user_data()  # Load all user data
    user = next((u for u in user_data['users'] if u['username'] == username), None)  # Find the specific user

    if not user:  # If user not found, log and exit
        print(f"User '{username}' not found.")
        return

    reminders_sent = user.get("reminders_sent", 0)  # Track reminders sent
    if reminders_sent >= NOTIFICATION_LIMIT:  # Stop if limit reached
        print(f"Max reminders sent for '{username}'.")
        return

    # Fetch user's daily water target and phone number
    daily_target = user.get("daily_target", 0)
    phone_number = user.get("phone_number", "Unknown Number")
    if daily_target <= 0:  # Validate the water target
        print(f"No valid daily water target found for '{username}'.")
        return

    # Calculate water intake per reminder
    water_per_notification = round(daily_target / NOTIFICATION_LIMIT, 2)

    # Get a motivational quote
    motivational_message = get_random_quote(max_length=150)
    if isinstance(motivational_message, dict):  # Handle API error
        motivational_message = "Stay hydrated! Health is wealth."

    # Construct the reminder message
    reminder_message = (
        f"{motivational_message} Don't forget to drink approximately {water_per_notification} liters of water."
    )

    # Send the SMS
    response = send_sms(phone_number, reminder_message)
    if response.get("status") == "Error":  # Handle SMS errors
        print(f"Failed to send SMS to {username}: {response.get('description')}")
    else:
        print(f"SMS successfully sent to {username}: {reminder_message}")

    # Update reminder count and save user data
    user["reminders_sent"] = reminders_sent + 1
    save_user_data(user_data)


def schedule_reminders():
    """
    Schedule reminders for all users at regular intervals.
    """
    user_data = load_user_data()  # Load all user data
    for username in user_data['users']:
        # Schedule reminders at the defined interval
        schedule.every(NOTIFICATION_INTERVAL_MINUTES).minutes.do(send_reminder, username=username["username"])


if __name__ == "__main__":
    # Initialize the reminders_sent count for all users
    user_data = load_user_data()
    for user in user_data['users']:
        user["reminders_sent"] = 0
    save_user_data(user_data)  # Save initialized data

    print("Starting AquaMind Reminder Scheduler...")
    schedule_reminders()

    # Run the scheduler continuously
    while True:
        schedule.run_pending()
        time.sleep(1)  # Avoid high CPU usage by sleeping between checks