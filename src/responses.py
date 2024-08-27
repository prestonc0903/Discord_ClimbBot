from random import choice, randint
from db_operations import get_user
from workout_functions import generate_warmup, generate_boulder_routine, generate_toprope_routine, generate_cooldown_routine

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    else:
        return choice(['I do not understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])

async def get_profile(message, user_message, user_state):
    try:
        # Split the user message to get the first and last name
        first_name, last_name = user_message.split(' ', 1) 
        # Retrieve user data using Discord ID
        user = get_user(str(message.author.id))  # Using Discord ID to get the user

        # Check if the user was found and matches the provided name
        if user and user['discord_id'] == str(message.author.id):
            if first_name.lower() == user['first_name'].lower() and last_name.lower() == user['last_name'].lower():
                # Construct the profile response
                response = (f"First Name: {user['first_name'].capitalize()}\n"
                            f"Last Name: {user['last_name'].capitalize()}\n"
                            f"Age: {user['age']}\n"
                            f"Weight: {user['weight']} kg\n"
                            f"Height: {user['height']} cm\n"
                            f"Years Climbing: {user['years_climbing']}\n"
                            f"Boulder Grade: {user['boulder_grade']}\n"
                            f"Top Rope Grade: {user['top_rope_grade']}")
            else:
                response = "The name you provided does not match your profile."
        else:
            response = "No profile found or profile does not match your Discord ID."
        
        # Send the profile information or error message
        await message.channel.send(response)
        user_state['state'] = None
    
    except ValueError:
        await message.channel.send("Invalid entry. Please provide the first and last name as two words.")

def create_workout(climber_level, workout_type):
    if workout_type == 'boulder':
        warmup = generate_warmup(climber_level)
        climb = generate_boulder_routine(climber_level)
        cooldown = generate_cooldown_routine()
        
        # Create formatted strings for each part of the workout
        warmup_str = "\n".join(f"- {exercise}" for exercise in warmup)
        climb_str = "\n".join(f"- {route}" for route in climb)
        cooldown_str = "\n".join(f"- {exercise}" for exercise in cooldown)

        # Combine all parts into a single formatted string
        workout_message = (
            "**Workout Plan**\n\n"
            "**Based on your current bouldering level, here's a workout plan that will help you get to the next level**\n\n"
            "**Warm-up:**\n" + warmup_str + "\n\n"
            "**Climbing Routine:**\n" + climb_str + "\n\n"
            "**Cooldown:**\n" + cooldown_str
        )
        return workout_message
    elif workout_type == 'top_rope':
        warmup = generate_warmup(climber_level)
        climb = generate_toprope_routine(climber_level)
        cooldown = generate_cooldown_routine()
        
        # Create formatted strings for each part of the workout
        warmup_str = "\n".join(f"- {exercise}" for exercise in warmup)
        climb_str = "\n".join(f"- {route}" for route in climb)
        cooldown_str = "\n".join(f"- {exercise}" for exercise in cooldown)

        # Combine all parts into a single formatted string
        workout_message = (
            "**Workout Plan**\n\n"
            "**Based on your current top rope level, here's a workout plan that will help you get to the next level**\n\n"
            "**Warm-up:**\n" + warmup_str + "\n\n"
            "**Climbing Routine:**\n" + climb_str + "\n\n"
            "**Cooldown:**\n" + cooldown_str
        )
        return workout_message