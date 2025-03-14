import cv2
import numpy as np
from cryptography.fernet import Fernet
import os

# -------------------- Encryption / Decryption --------------------
def generate_key():
    """Generate an encryption key and save it to a file (Run once)."""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load the encryption key."""
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """Encrypt a message using AES encryption."""
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    """Decrypt a message using AES encryption."""
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message.encode()).decode()

# -------------------- Steganography Encoding --------------------
def text_to_binary(text):
    """Convert text into binary."""
    return ''.join(format(ord(char), '08b') for char in text)

def hide_text(image_path, secret_text, output_image):
    """Embed secret text into an image using LSB steganography."""
    img = cv2.imread(image_path)
    binary_text = text_to_binary(secret_text) + '1111111111111110'  # End delimiter

    data_index = 0
    for row in img:
        for pixel in row:
            for i in range(3):  # Iterate over RGB channels
                if data_index < len(binary_text):
                    pixel[i] = (pixel[i] & 0b11111110) | int(binary_text[data_index])  # Modify LSB
                    data_index += 1

    cv2.imwrite(output_image, img)
    print(f"✅ Secret message hidden successfully in '{output_image}'")

# -------------------- Steganography Decoding --------------------
def binary_to_text(binary):
    """Convert binary string to text."""
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

def extract_text(image_path):
    """Extract hidden text from an image."""
    img = cv2.imread(image_path)
    binary_text = ""

    for row in img:
        for pixel in row:
            for i in range(3):  # Iterate over RGB channels
                binary_text += str(pixel[i] & 1)  # Extract LSB
                if binary_text[-16:] == "1111111111111110":  # Stop at delimiter
                    return binary_to_text(binary_text[:-16])

    return "❌ No hidden message found"

# -------------------- User Interaction --------------------
if __name__ == "__main__":
    generate_key()  # Run once to create encryption key

    print("\n🔹 Image Steganography 🔹")
    print("1️⃣ Hide Message in Image")
    print("2️⃣ Extract Message from Image")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        image_path = input("Enter input image path: ")
        secret_message = input("Enter secret message: ")

        encrypt_option = inp
        ut("Do you want to encrypt the message? (yes/no): ").lower()
        if encrypt_option == "yes":
            secret_message = encrypt_message(secret_message)

        output_image = "stego_image.png"
        hide_text(image_path, secret_message, output_image)

    elif choice == "2":
        stego_image = input("Enter stego image path: ")
        extracted_message = extract_text(stego_image)

        decrypt_option = input("Is this an encrypted message? (yes/no): ").lower()
        if decrypt_option == "yes":
            extracted_message = decrypt_message(extracted_message)

        print(f"🔓 Hidden Message: {extracted_message}")

    else:
        print("❌ Invalid choice. Please enter 1 or 2.")
