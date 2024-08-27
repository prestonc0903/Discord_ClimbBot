import sqlite3
import logging

DATABASE = 'users.db'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def create_user(discord_id, first_name, last_name, age, weight, height, years_climbing, boulder_grade, top_rope_grade):
    """Insert a new user into the database if they don't already have an account."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            # Check if the user already has an account
            cursor.execute('SELECT * FROM users WHERE discord_id = ?', (discord_id,))
            existing_user = cursor.fetchone()
            if existing_user:
                logging.info(f"User with Discord ID {discord_id} already has an account.")
                return False
            # Insert the new user
            cursor.execute('''
            INSERT INTO users (discord_id, first_name, last_name, age, weight, height, years_climbing, boulder_grade, top_rope_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (discord_id, first_name, last_name, age, weight, height, years_climbing, boulder_grade, top_rope_grade))
            conn.commit()
            logging.info(f"User {first_name} {last_name} created successfully.")
            return True
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return False

def get_user(discord_id):
    """Retrieve a user by Discord ID."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE discord_id = ?', (discord_id,))
            row = cursor.fetchone()
            if row:
                logging.info(f"User with Discord ID {discord_id} retrieved successfully.")
                # Convert row to dictionary
                user = {
                    'discord_id': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'age': row[4],
                    'weight': row[5],
                    'height': row[6],
                    'years_climbing': row[7],
                    'boulder_grade': row[8],
                    'top_rope_grade': row[9]
                }
                return user
            else:
                logging.info(f"No profile found for Discord ID {discord_id}.")
                return None
    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        return None

def update_user(discord_id, field, new_value):
    """Update a specific field for a user by Discord ID."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            query = f'UPDATE users SET {field} = ? WHERE discord_id = ?'
            cursor.execute(query, (new_value, discord_id))
            conn.commit()
            logging.info(f"Updated {field} for Discord ID {discord_id} to {new_value}.")
    except Exception as e:
        logging.error(f"Error updating user: {e}")