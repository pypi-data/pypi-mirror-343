import re
import hashlib

def is_strong_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[^A-Za-z0-9]", password)):
        return False
    return True

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

