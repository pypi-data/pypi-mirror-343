# 🔒 Password Manager CLI Application

A secure and simple **Password Manager** built with **Python** for managing your credentials directly from the **command line interface (CLI)**.  
Features include:
- Master password protection 🔐
- Password strength checking 🛡️
- Expiration and rotation warnings for old passwords 📅
- Beautiful and clean CLI prompts ✨

---

## 📦 Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
```bash
git clone https://github.com/santhoshandavar10/PasswordManager.git
cd PasswordManager

2. Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate    # For Mac/Linux
venv\Scripts\activate       # For Windows

3.Install required dependencies:

pip install -r requirements.txt


🚀 How to Run
After installing:

python main.py

✅ First time, you will be asked to create a Master Password.
✅ After setup, you can store, view, update, and manage your passwords securely.

⚡ Features
Master Password Protection: Keeps your database locked.

Password Strength Checker: Ensures your passwords are strong enough.

Expiration System: Warns you when stored passwords are old and need to be updated.

Simple CLI Design: No GUI needed, super lightweight.

Secure Storage: Passwords stored safely in a local JSON database.

📂 Project Structure

PasswordManager/
├── dist/           # (For compiled executable, optional)
├── venv/           # (Virtual environment files)
├── main.py         # Main application code
├── passwords.json  # Password database (auto-created)
├── master.json     # Master password (encrypted)
├── requirements.txt
└── README.md

🔥 Future Improvements (Ideas)
Encryption of passwords using cryptography.

Multi-user support.

Auto-logout after inactivity.

🤝 Contributing
Pull requests are welcome! Feel free to open issues or suggest improvements.

📜 License
This project is licensed under the MIT License.

🙋‍♂️ Author
Built with ❤️ by Santhosh Andavar

