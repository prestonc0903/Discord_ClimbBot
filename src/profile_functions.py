from db_operations import create_user, get_user, update_user
from responses import create_workout
async def handle_register(message, user_message, user_states):
    """ Handle user registration process. """
    username = str(message.author)
    discord_id = str(message.author.id)  # Get the Discord ID of the user
    user_state = user_states.get(username, {'state': None, 'data': {}})

    # Check if user already has a profile
    existing_user = get_user(discord_id)
    if existing_user:
        await message.channel.send("You already have profile under this Discord Account. Use !profile to view your details.")
        user_states[username] = {'state': None, 'data': {}}
        return

    # Register Name
    if user_state['state'] == 'register_name':
        try:
            first_name, last_name = user_message.split(' ', 1)
            user_state['data']['first_name'] = first_name.lower()
            user_state['data']['last_name'] = last_name.lower()
            user_state['state'] = 'register_age'
            await message.channel.send(f"Hello {first_name} {last_name}, please provide your age.")
        except ValueError:
            await message.channel.send("Invalid entry. Please provide your first and last name.")

    # Register Age
    elif user_state['state'] == 'register_age':
        try:
            age = int(user_message)
            if age >= 0:
                user_state['data']['age'] = age
                user_state['state'] = 'register_weight'
                await message.channel.send("Thanks. Please provide your weight in kilograms (kg).")
            else:
                await message.channel.send("Age cannot be negative. Please provide a valid age.")
        except ValueError:
            await message.channel.send("Invalid entry. Please provide a valid number.")

    # Register Weight
    elif user_state['state'] == 'register_weight':
        try:
            weight = float(user_message)
            if weight > 0:
                user_state['data']['weight'] = weight
                user_state['state'] = 'register_height'
                await message.channel.send("Thanks. Please provide your height in centimeters (cm).")
            else:
                await message.channel.send("Weight must be positive. Please provide a valid weight.")
        except ValueError:
            await message.channel.send("Invalid entry. Please provide a valid number.")

    # Register Height
    elif user_state['state'] == 'register_height':
        try:
            height = float(user_message)
            if height > 0:
                user_state['data']['height'] = height
                user_state['state'] = 'register_years_climbing'
                await message.channel.send("Thanks. Please provide your years of climbing experience.")
            else:
                await message.channel.send("Height must be positive. Please provide a valid height.")
        except ValueError:
            await message.channel.send("Invalid entry. Please provide a valid number.")

    # Register Years of Climbing Experience
    elif user_state['state'] == 'register_years_climbing':
        try:
            years_climbing = int(user_message)
            if years_climbing >= 0:
                user_state['data']['years_climbing'] = years_climbing
                user_state['state'] = 'register_boulder_grade'
                await message.channel.send("Thanks. Please provide your boulder grade (v0 - v12).")
            else:
                await message.channel.send("Years of climbing experience cannot be negative. Please provide a valid number.")
        except ValueError:
            await message.channel.send("Invalid entry. Please provide a valid number.")

    # Register Boulder Grade
    elif user_state['state'] == 'register_boulder_grade':
        boulder_grade = user_message
        user_state['data']['boulder_grade'] = boulder_grade
        user_state['state'] = 'register_top_rope_grade'
        await message.channel.send("Thanks. Please provide your top rope grade (5.8 - 5.12).")

    # Register Top Rope Grade
    elif user_state['state'] == 'register_top_rope_grade':
        top_rope_grade = user_message
        user_state['data']['top_rope_grade'] = top_rope_grade
        user_data = user_state['data']

        # Create the new user
        create_user(discord_id, user_data['first_name'], user_data['last_name'], user_data['age'], user_data['weight'],
                    user_data['height'], user_data['years_climbing'], user_data['boulder_grade'], user_data['top_rope_grade'])

        await message.channel.send(f"User {user_data['first_name']} {user_data['last_name']} registered successfully!")
        user_state['state'] = None
        user_state['data'] = {}

    else:
        await message.channel.send("To start registration, use the command !register.")
        user_state['state'] = None
        user_state['data'] = {}

async def handle_update(message, user_message, user_states):
    """ Handle user profile update process. """
    username = str(message.author)
    discord_id = str(message.author.id)
    user_state = user_states.get(username, {'state': None, 'data': {}})
    user = get_user(discord_id)

    if not user:
        await message.channel.send("No profile found for your Discord ID. Use !register to create a new profile.")
        user_states[username] = {'state': None, 'data': {}}
        return

    if user_state['state'] == 'update_field':
        field_to_update = user_message.lower()
        if field_to_update in ['first_name', 'last_name', 'age', 'weight', 'height', 'years_climbing', 'boulder_grade', 'top_rope_grade']:
            user_state['state'] = 'update_value'
            user_state['data']['field'] = field_to_update
            await message.channel.send(f"Please provide a new value for {field_to_update.replace('_', ' ')}.")
        else:
            await message.channel.send("Invalid field. Please specify one of: first_name, last_name, age, weight, height, years_climbing, boulder_grade, top_rope_grade.")

    elif user_state['state'] == 'update_value':
        field = user_state['data'].get('field')
        new_value = user_message

        # Apply validations similar to registration
        if field == 'age' or field == 'years_climbing':
            try:
                new_value = int(new_value)
                if new_value < 0:
                    raise ValueError
            except ValueError:
                await message.channel.send("Please provide a valid non-negative integer.")
                return
        elif field in ['weight', 'height']:
            try:
                new_value = float(new_value)
                if new_value <= 0:
                    raise ValueError
            except ValueError:
                await message.channel.send("Please provide a valid positive number.")
                return

        update_user(discord_id, field, new_value)
        await message.channel.send(f"Your {field.replace('_', ' ')} has been updated to {new_value}.")
        user_state['state'] = None
        user_state['data'] = {}

    else:
        user_state['state'] = 'update_field'
        await message.channel.send("Which field would you like to update? (first_name, last_name, age, weight, height, years_climbing, boulder_grade, top_rope_grade)")

async def handle_workout_generation(message, user_states, workout_type):
    """ Handle the workout generation process. """
    username = str(message.author)
    discord_id = str(message.author.id)
    user_state = user_states.get(username, {'state': None, 'data': {}})
    user = get_user(discord_id)
    
    if not user:
        await message.channel.send("No profile found for your Discord ID. Use !register to create a new profile.")
        user_states[username] = {'state': None, 'data': {}}
        return

    # Bouldering workout
    if workout_type == 'boulder':
        climber_boulder_experience = user.get('boulder_grade', 'v0')

        try:
            # Generate the workout based on experience level
            workout_message = create_workout(climber_boulder_experience, workout_type)
            await message.channel.send(workout_message)
            
        except ValueError as e:
            await message.channel.send(str(e))
            user_states[username]['state'] = None  # Reset state on error

    # Top rope workout
    elif workout_type == 'top_rope':
        climber_top_rope_experience = user.get('top_rope_grade', '5.0')

        try:
            # Generate the workout based on experience level
            workout_message = create_workout(climber_top_rope_experience, workout_type)
            await message.channel.send(workout_message)

        except ValueError as e:
            await message.channel.send(str(e))
            user_states[username]['state'] = None  # Reset state on error

    else:
        await message.channel.send("Invalid workout type specified.")
        user_state['state'] = None
        user_state['data'] = {}
    user_state['state'] = None
    user_state['data'] = {}