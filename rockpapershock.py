import os
import random
import requests
from dotenv import load_dotenv

ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')

def load_env():
    """Loads the API key and Shock ID from the .env file."""
    if os.path.exists(ENV_FILE):
        load_dotenv(ENV_FILE)
        api_key = os.getenv('SHOCK_API_KEY')
        shock_id = os.getenv('SHOCK_ID')
        return api_key, shock_id
    return None, None

def trigger_shock(api_key, shock_id, intensity, duration, shock_type='Shock'):
    """Sends a shock or vibrate command to the OpenShock API."""
    print(f"Sending {shock_type.lower()} with intensity: {intensity} and duration: {duration} milliseconds")

    url = 'https://api.shocklink.net/2/shockers/control'
    headers = {
        'accept': 'application/json',
        'OpenShockToken': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'shocks': [{
            'id': shock_id,
            'type': shock_type,
            'intensity': intensity,
            'duration': duration,
            'exclusive': True
        }],
        'customName': 'RockPaperShock'
    }

    response = requests.post(url=url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'{shock_type} sent successfully.')
    else:
        print(f"Failed to send {shock_type.lower()}. Response: {response.content}")

def get_user_choice():
    """Prompts the user to choose rock, paper, or scissors."""
    while True:
        choice = input("Enter your choice (rock/paper/scissors): ").lower()
        if choice in ['rock', 'paper', 'scissors']:
            return choice
        print("Invalid choice. Please enter rock, paper, or scissors.")

def get_computer_choice():
    """Randomly selects the computer's choice."""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    """Determines the winner of the game."""
    if user_choice == computer_choice:
        return "tie"
    elif (
        (user_choice == "rock" and computer_choice == "scissors") or
        (user_choice == "scissors" and computer_choice == "paper") or
        (user_choice == "paper" and computer_choice == "rock")
    ):
        return "user"
    else:
        return "computer"

def play_game(api_key, shock_id):
    """Plays a single round of rock-paper-shock."""
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()

    print(f"You chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")

    result = determine_winner(user_choice, computer_choice)

    if result == "tie":
        print("It's a tie!")
    elif result == "user":
        print("You win!")
        trigger_shock(api_key, shock_id, 100, 1000, 'Vibrate')
    else:
        print("You lose!")
        trigger_shock(api_key, shock_id, 50, 1000, 'Shock')

def main():
    api_key, shock_id = load_env()

    if not api_key or not shock_id:
        print("API key or Shock ID not found. Please set up your .env file.")
        return

    print("Welcome to Rock Paper Shock!")
    print("Win: You get a vibration. Lose: You get a shock. Tie: Nothing happens.")

    while True:
        play_game(api_key, shock_id)
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
