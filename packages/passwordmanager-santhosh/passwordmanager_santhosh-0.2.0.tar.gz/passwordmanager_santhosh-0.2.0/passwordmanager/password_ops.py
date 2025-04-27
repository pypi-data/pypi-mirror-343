import json
import os
import random
import string
import time
from passwordmanager.utils import is_strong_password

PASSWORD_FILE = os.path.join(os.path.dirname(__file__), 'storage', 'passwords.json')

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def save_password(account, username, password):
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            try:
                passwords = json.load(f)
            except json.JSONDecodeError:
                passwords = {}
    else:
        passwords = {}

    passwords[account] = {
        "username": username,
        "password": password,
        "last_updated": time.ctime()
    }

    with open(PASSWORD_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

def generate_and_save_password():
    account = input("🔑 Enter Account Name: ")
    username = input("👤 Enter Username/Email: ")
    password = generate_password()
    print(f"Generated Password: {password}")

    save_password(account, username, password)
    print("✅ Password Saved Successfully!")

def show_passwords():
    if not os.path.exists(PASSWORD_FILE):
        print("⚠️ No passwords saved yet.")
        return

    with open(PASSWORD_FILE, "r") as f:
        passwords = json.load(f)

    if not passwords:
        print("⚠️ No passwords saved yet.")
        return

    for account, info in passwords.items():
        print("\n🔑 Account:", account)
        print("👤 Username:", info['username'])
        print("🔒 Password:", info['password'])
        print("🕒 Last Updated:", info['last_updated'])
        print("-" * 30)
