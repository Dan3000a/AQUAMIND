def calculate_daily_intake(gender, age, weight):
    """Calculate the daily water intake target based on gender, age, and weight."""

    # Default daily intake based on age and gender
    if age <= 13:
        if gender == 'male':
            daily_target = 2.1  # male under 14
        else:
            daily_target = 1.9  # female under 14
    else:
        if gender == 'male':
            daily_target = 2.5  # male 14 and above
        else:
            daily_target = 2.0  # female 14 and above

    # Adjust based on weight (e.g., 30 mL per kg)
    daily_target = max(daily_target, weight * 0.03)

    return daily_target
