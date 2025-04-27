import os
import hashlib
import getpass

MASTER_PASS_FILE = os.path.join(os.path.dirname(__file__), 'storage', 'master.key')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def set_master_password():
    print("\n🔐 No master password found. Let's create one.")
    while True:
        master = getpass.getpass("Set your master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        if master == confirm:
            with open(MASTER_PASS_FILE, "w") as f:
                f.write(hash_password(master))
            print("✅ Master password set successfully!")
            break
        else:
            print("❌ Passwords do not match. Try again.")

def verify_master_password():
    if not os.path.exists(MASTER_PASS_FILE):
        return False

    stored_hash = open(MASTER_PASS_FILE, "r").read().strip()
    for attempt in range(3):
        master = getpass.getpass("Enter master password: ")
        if hash_password(master) == stored_hash:
            print("✅ Access granted!")
            return True
        else:
            print("❌ Incorrect password. Try again.")

    print("❌ Too many attempts. Exiting...")
    exit()
