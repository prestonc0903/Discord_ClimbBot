import random

boulder_grade = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11']
top_rope_grade = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']

arm_warmup = ['Cross-Body Shoulder Stretch', 'Shoulder Rolls', 'Forward Arm Circles', 'Reverse Arm Circles',
              'Chest Horizontal Band Stretch', 'Overhead Horizontal Band Stretch']
body_warmup = ['Squats', 'Lunge', 'Hamstring Hip Flexor Stretch', 'Pigeon Both Sides', 'Full Fold', 
              'Childs Pose', 'Back Stretch']
hangboard_easy = ['Hangboard Full Grip', 'Hangboard 4-Finger Open Grip', 'Hangboard 3-Finger Pocket']
hangboard_hard = ['Hangboard 12mm Crimp Grip', 'Hangboard 8mm Crimp Grip', 'Hangboard 6mm Crimp Grip', 'Hangboard 2-Finger Pocket']

warmup_patterns = {
    'beginner': [arm_warmup, hangboard_easy, arm_warmup, body_warmup, body_warmup, hangboard_easy, arm_warmup, hangboard_hard, body_warmup, body_warmup, arm_warmup, hangboard_easy],
    'intermediate': [arm_warmup, hangboard_easy, hangboard_easy, body_warmup, body_warmup, arm_warmup, hangboard_easy, hangboard_hard, hangboard_hard, body_warmup, body_warmup, arm_warmup],
    'experienced': [arm_warmup, body_warmup, body_warmup, arm_warmup, hangboard_easy, hangboard_easy, body_warmup, body_warmup, arm_warmup, hangboard_hard, hangboard_hard, hangboard_hard],
}

def generate_warmup(experience):
    warmup = []
    if experience in boulder_grade[0:3] or experience in top_rope_grade[0:6]:
        experience_level = 'beginner'
    elif experience in boulder_grade[3:6] or experience in top_rope_grade[6:12]:
        experience_level = 'intermediate'
    elif experience in boulder_grade[6:] or experience in top_rope_grade[12:]:
        experience_level = 'experienced'
    else:
        raise ValueError(f"Invalid experience level: {experience}")

    pattern = warmup_patterns[experience_level]
    
    for item_list in pattern:
        warmup.append(random.choice(item_list))
    
    return warmup

def generate_boulder_routine(experience):
    # Define difficulty levels around the input level
    levels = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12']
    
    if experience not in levels:
        raise ValueError("Invalid climbing level. Please enter a valid level like 'v0', 'v3', or 'v5'.")

    # Find the index of the user's climbing level
    level_index = levels.index(experience)

    # Create a base routine depending on the experience level
    if level_index <= 5:  # For climbers from v0 to v5
        routine = ['v0', 'v0', 'v1', 'v1']
    elif level_index <= 8:  # For climbers from v6 to v8
        routine = ['v1', 'v1', 'v2', 'v3']
    else:  # For climbers from v9 and up
        routine = ['v2', 'v2', 'v4', 'v6']

    # Create a routine with a mix of lower, equal, and slightly higher difficulties
    for _ in range(10):
        difficulty = random.choices(
            levels[max(0, level_index - 2): min(len(levels), level_index + 3)],
            weights=[1, 2, 4, 2, 1]  # Weights favoring the user's level
        )[0]
        routine.append(difficulty)
    return routine

def generate_toprope_routine(experience):
    # Define difficulty levels around the input level
    levels = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    
    if experience not in levels:
        raise ValueError("Invalid climbing level. Please enter a valid level like '5.4', '5.10', or '5.12'.")

    # Find the index of the user's climbing level
    level_index = levels.index(experience)

    # Create a base routine depending on the experience level
    if level_index <= 5:  # For climbers from 5.0 to 5.5
        routine = ['5.0', '5.1']
    elif level_index <= 8:  # For climbers from 5.6 to 5.8
        routine = ['5.4', '5.6']
    elif level_index <= 11:  # For climbers from 5.9 to 5.11
        routine = ['5.8', '5.8']
    else:  # For climbers from 5.12 and up
        routine = ['5.9', '5.10']

    # Create a routine with a mix of lower, equal, and slightly higher difficulties
    for _ in range(4):
        difficulty = random.choices(
            levels[max(0, level_index - 2): min(len(levels), level_index + 3)],
            weights=[1, 2, 4, 2, 1]  # Weights favoring the user's level
        )[0]
        routine.append(difficulty)
    return routine

def generate_cooldown_routine():

    # Define cooldown components
    stretching_exercises = [
        "Forearm Stretch each side",
        "Cat-Cow Stretch",
        "Hip Flexor Stretch each side",
        "Shoulder Stretch each side",
        "Hamstring Stretch each side",
        "Chest Stretch each side",
        "Calf Stretch each side"
    ]
    foam_rolling_exercises = [
        "Forearm foam rolling each side",
        "Upper back foam rolling",
        "Calf foam rolling each side",
        "Quadriceps foam rolling each side",
        "Hamstring foam rolling each side"
    ]
    hangboard_easy = ['Hangboard Full Grip', 'Hangboard 4-Finger Open Grip', 'Hangboard 3-Finger Pocket']

    # Randomly select exercises
    cooldown_routine = []
    cooldown_routine.extend(random.sample(stretching_exercises, 2))  # Pick 2 random stretches
    cooldown_routine.extend(random.sample(hangboard_easy, 2))  # Pick 2 random hangboarding exercise
    cooldown_routine.extend(random.sample(foam_rolling_exercises, 2))  # Pick 2 random foam rolling exercises
    
    return cooldown_routine

