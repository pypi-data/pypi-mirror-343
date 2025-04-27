from passwordmanager.security import verify_master_password, set_master_password
from passwordmanager.password_ops import generate_and_save_password, show_passwords
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    if not verify_master_password():
        set_master_password()

    print(Fore.CYAN + "\n🔐 Welcome to Password Manager CLI 🔐")
    print("=" * 40)

    while True:
        print(Fore.YELLOW + """
1️⃣ Generate and Save New Password
2️⃣ View Saved Passwords
3️⃣ Exit
""")
        choice = input(Fore.GREEN + "Please select an option (1-3): ").strip()

        if choice == '1':
            generate_and_save_password()
        elif choice == '2':
            show_passwords()
        elif choice == '3':
            print(Fore.BLUE + "👋 Exiting Password Manager. Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "❌ Invalid choice! Please try again.")
