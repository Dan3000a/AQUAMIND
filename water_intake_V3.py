import json


def calculate_water_intake(age, gender, weight):
    """
    Calculate daily water intake based on age, gender, weight, and pregnancy status.
    Args:
        age (int): User's age in years.
        gender (str): User's gender ('male' or 'female').
        weight (float): User's weight in kilograms.
    Returns:
        float: Daily water intake in liters.
    """
    if gender.lower() == 'male':
        if age < 18:
            water_intake = weight * 0.04  # 40 ml per kg for children
        else:
            water_intake = 3.7  # 3.7 liters for adult men
    elif gender.lower() == 'female':
        if age < 18:
            water_intake = weight * 0.04  # 40 ml per kg for children
        else:
            pregnant = input("Are you pregnant? (yes/no): ").lower() == 'yes'
            water_intake = 3.0 if pregnant else 2.7  # Adjust for pregnancy
    else:
        raise ValueError("Invalid gender. Please specify 'male' or 'female'.")

    return water_intake


def register_user(username, phone_number, gender, age, weight):
    """
    Register a new user with their daily water intake target.
    Args:
        username (str): User's name.
        phone_number (str): User's phone number.
        gender (str): User's gender.
        age (int): User's age.
        weight (float): User's weight.
    Returns:
        str: Welcome message or error message.
    """
    if gender not in ['male', 'female']:
        return "Invalid gender. Please enter 'male' or 'female'."
    if not (0 < age < 150):
        return "Invalid age. Please enter a valid age."
    if weight <= 0:
        return "Invalid weight. Please enter a positive weight."

    daily_target = calculate_water_intake(age, gender, weight)

    try:
        with open('users.json', 'r+') as file:
            data = json.load(file)
            user_id = len(data['users']) + 1
            new_user = {
                "id": user_id,
                "username": username,
                "phone_number": phone_number,
                "gender": gender,
                "age": age,
                "weight": weight,
                "daily_target": daily_target,
                "water_intake": 0.0
            }
            data['users'].append(new_user)
            file.seek(0)
            json.dump(data, file, indent=4)

        return f"Welcome, {username}! Your daily water intake target is {daily_target:.2f} liters."
    except FileNotFoundError:
        return "Error: 'users.json' file not found."
    except json.JSONDecodeError:
        return "Error: Failed to decode 'users.json'."
    except Exception as e:
        return f"Unexpected error: {e}"