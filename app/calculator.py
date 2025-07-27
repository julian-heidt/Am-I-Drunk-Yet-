WIDMARK_FACTOR_MALE = 0.68
WIDMARK_FACTOR_FEMALE = 0.55
WIDMARK_FACTOR_OTHER = (WIDMARK_FACTOR_MALE + WIDMARK_FACTOR_FEMALE) / 2
TARGET_BAC = 0.1
ALCOHOL_GRAMS_PER_DRINK = 14.0
METABOLISM_RATE = 0.015  # % per hour

def get_widmark_factor(gender):
    """Gets the Widmark factor based on gender."""
    gender_lower = gender.lower()
    if gender_lower == 'male':
        return WIDMARK_FACTOR_MALE
    elif gender_lower == 'female':
        return WIDMARK_FACTOR_FEMALE
    else:
        return WIDMARK_FACTOR_OTHER

def calculate_drinks_to_target_bac(weight, gender, current_drinks):
    """
    Calculates the number of additional standard drinks to reach a BAC of 0.1%.
    Assumes weight is in kilograms.
    """
    r = get_widmark_factor(gender)
    
    # Weight in grams
    weight_grams = weight * 1000

    # Total alcohol in grams to reach target BAC
    total_alcohol_grams = (TARGET_BAC / 100) * weight_grams * r

    # Total number of drinks to reach target
    total_drinks = total_alcohol_grams / ALCOHOL_GRAMS_PER_DRINK
    
    # Additional drinks needed
    additional_drinks = total_drinks - current_drinks
    
    # If the user is already at or above the target, they need 0 more drinks.
    if additional_drinks < 0:
        return 0
        
    return round(additional_drinks, 1)

def calculate_time_to_sober(current_drinks, weight, gender):
    """
    Calculates the time in hours for BAC to return to zero.
    Assumes weight is in kilograms.
    """
    if current_drinks <= 0:
        return 0

    r = get_widmark_factor(gender)
    
    # Weight in grams
    weight_grams = weight * 1000

    # Total alcohol consumed in grams
    total_alcohol_grams = current_drinks * ALCOHOL_GRAMS_PER_DRINK

    # Current BAC
    current_bac = (total_alcohol_grams / (weight_grams * r)) * 100

    # Time to sober in hours
    time_to_sober = current_bac / METABOLISM_RATE

    return round(time_to_sober, 1)
