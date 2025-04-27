import os
import json
import time
import getpass
from .utils import is_strong_password, hash_password
from .other_modules import generate_password, save_password, load_passwords, show_passwords

MASTER_PASSWORD_FILE = "master_password.json"
PASSWORD_DB_FILE = "passwords.json"
PASSWORD_EXPIRY_DAYS = 90  # Password rotation threshold

def set_master_password():
    print("No master password found! Let's create one.")
    while True:
        password = getpass.getpass("Set your master password: ")
        if is_strong_password(password):
            hashed = hash_password(password)
            with open(MASTER_PASSWORD_FILE, "w") as f:
                json.dump({"hash": hashed}, f)
            break
        else:
            print("❌ Password not strong enough. Try again.")

def verify_master_password():
    with open(MASTER_PASSWORD_FILE, "r") as f:
        data = json.load(f)
    for _ in range(3):
        password = getpass.getpass("Enter master password: ")
        if hash_password(password) == data["hash"]:
            print("✅ Access granted!\n")
            return True
        else:
            print("❌ Wrong password.")
    return False

def main():
    if not os.path.exists(MASTER_PASSWORD_FILE):
        set_master_password()

    if not verify_master_password():
        print("Too many failed attempts. Exiting.")
        return

    passwords = load_passwords()

    while True:
        print("\n🔐 Password Manager Menu:")
        print("1. Generate and save a new password")
        print("2. Show saved passwords")
        print("3. Exit")

        choice = input("Enter choice (1-3): ")

        if choice == "1":
            name = input("Enter name for the account (e.g., Gmail): ")
            new_password = generate_password()
            print(f"Generated Password: {new_password}")
            save_password(name, new_password, passwords)
        elif choice == "2":
            show_passwords(passwords)
        elif choice == "3":
            print("👋 Exiting Password Manager.")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
