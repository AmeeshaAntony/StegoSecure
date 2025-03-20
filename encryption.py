import os
import time
from cryptography.fernet import Fernet

def generate_key():
    """Generate and save encryption key."""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load encryption key from file."""
    return open("secret.key", "rb").read()

def encrypt_message(message, expire_time):
    """Encrypt message with expiration timestamp."""
    key = load_key()
    cipher = Fernet(key)
    timestamp = str(int(time.time()) + expire_time)
    full_message = f"{timestamp}|{message}"
    return cipher.encrypt(full_message.encode()).decode()

def decrypt_message(encrypted_message):
    """Decrypt message and check expiration."""
    key = load_key()
    cipher = Fernet(key)
    try:
        decrypted_text = cipher.decrypt(encrypted_message.encode()).decode()
        timestamp, message = decrypted_text.split("|", 1)
        if int(timestamp) < time.time():
            return "❌ Expired Message!"
        return message
    except:
        return "❌ Decryption Failed!"
