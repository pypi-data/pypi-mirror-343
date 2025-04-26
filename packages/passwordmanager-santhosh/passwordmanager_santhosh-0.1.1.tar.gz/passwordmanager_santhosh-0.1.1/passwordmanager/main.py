# main.py
import json
import os
import time
from rich.console import Console
from rich.table import Table
from utils import is_strong_password
from master_password import verify_master_password

DATA_FILE = "passwords.json"
console = Console()

def load_passwords():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_passwords(passwords):
    with open(DATA_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

def add_password(passwords):
    site = console.input("[bold blue]🔹 Site name: [/bold blue]").lower()
    username = console.input("[bold blue]🔹 Username: [/bold blue]")
    password = console.input("[bold blue]🔹 Password: [/bold blue]")

    if not is_strong_password(password):
        console.print("[bold red]⚠️ Warning: Your password is weak. Consider making it stronger![/bold red]")

    passwords[site] = {
        "username": username,
        "password": password,
        "created_at": time.time()
    }
    save_passwords(passwords)
    console.print("[bold green]✅ Password saved![/bold green]")

def view_password(passwords):
    site = console.input("[bold blue]🔹 Enter site name to view: [/bold blue]").lower()
    if site in passwords:
        data = passwords[site]
        table = Table(title=f"🔑 Password Info for {site.capitalize()}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Username", data["username"])
        table.add_row("Password", data["password"])
        console.print(table)

        age = (time.time() - data.get("created_at", time.time())) / (60*60*24)
        if age > 90:
            console.print("[bold red]⚠️ Warning: Password is older than 90 days. Rotate it![/bold red]")
    else:
        console.print("[bold red]❌ No password stored for this site.[/bold red]")

def main():
    print("Welcome to Password Manager CLI!")
    verify_master_password()
    passwords = load_passwords()

    while True:
        console.print("\n[bold yellow]What do you want to do?[/bold yellow]")
        console.print("[blue]1.[/blue] Add new password")
        console.print("[blue]2.[/blue] View saved password")
        console.print("[blue]3.[/blue] Exit")
        choice = console.input("🔹 Choice (1/2/3): ")

        if choice == "1":
            add_password(passwords)
        elif choice == "2":
            view_password(passwords)
        elif choice == "3":
            console.print("[bold green]👋 Goodbye![/bold green]")
            break
        else:
            console.print("[bold red]❌ Invalid choice. Try again.[/bold red]")

if __name__ == "__main__":
    main()