import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
from responses import get_response, get_profile
from profile_functions import handle_register, handle_update, handle_workout_generation  # Import the handle_register function

# Load the Discord token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Dictionary to keep track of user states
user_states = {}

async def send_message(message: Message, user_message: str) -> None:
    response = get_response(user_message)
    await message.channel.send(response)

# Handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content.strip()
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    # Initialize user state if not present
    if username not in user_states:
        user_states[username] = {'state': None, 'data': {}}

    user_state = user_states[username]

    # Handle registration-related commands and states
    if user_message.startswith('!register'):
        user_states[username] = {'state': 'register_name', 'data': {}}
        await message.author.send("Please provide your first and last name.")
    elif user_state['state'] and user_state['state'].startswith('register'):
        await handle_register(message, user_message, user_states)

    # Handle profile updates
    elif user_message.startswith('!update'):
        user_states[username] = {'state': 'update_field', 'data': {}}
        await message.author.send("Which field would you like to update? (first_name, last_name, age, weight, height, years_climbing, boulder_grade, top_rope_grade)")
    elif user_state['state'] == 'update_field' or user_state['state'] == 'update_value':
        await handle_update(message, user_message, user_states)
    
    # View user profile
    elif user_message.startswith('!profile'):
        user_states[username] = {'state': 'profile_name'}
        await message.author.send("Please provide the first and last name of the profile you want to load.")
    elif user_state['state'] == 'profile_name':
        await get_profile(message, user_message, user_state)

    # Generate a workout for them.
    if user_message.startswith('!workout'):
        user_states[username] = {'state': 'workout', 'data': {}}
        await message.author.send("Do you want to boulder or top rope?")

    # Handle workout type response
    if user_state['state'] == 'workout':
        if user_message == 'boulder':
            user_state['state'] = 'boulder_workout'
            await message.author.send("Generating a boulder workout for you...")
            await handle_workout_generation(message, user_state, 'boulder')
        elif user_message == 'top rope':
            user_state['state'] = 'top_rope_workout'
            await message.author.send("Generating a top rope workout for you...")
            await handle_workout_generation(message, user_state, 'top_rope')
        else:
            await message.author.send("Invalid option. Please reply with 'boulder' or 'top rope'.")


################################################################################################################
#####NEXT PATCH
    ## Handle locate gym
    ##if user_message.startswith('!locate_gym'):
    ##    user_states[username] = {'state': 'locate', 'data': {}}
    ##    await message.author.send("Please provide a City and State and I will find some nearby gyms.")


# Main entry point
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
