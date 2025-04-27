import json
import random
import string
import time
import os

PASSWORD_FILE = "passwords.json"

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def save_password(account, username, password):
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            passwords = json.load(f)
    else:
        passwords = {}

    passwords[account] = {
        "username": username,
        "password": password,
        "last_updated": time.time()
    }

    with open(PASSWORD_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def show_passwords():
    passwords = load_passwords()
    if not passwords:
        print("No saved passwords found.")
    else:
        for account, info in passwords.items():
            print(f"🔑 Account: {account}")
            print(f"👤 Username: {info['username']}")
            print(f"🔒 Password: {info['password']}")
            print("-" * 30)
