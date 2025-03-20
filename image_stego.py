import os
import cv2
import numpy as np

def text_to_binary(text):
    """Convert text into binary (8-bit format)."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Convert binary string to readable text."""
    try:
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]  # Split into 8-bit chunks
        text = ''.join(chr(int(char, 2)) for char in chars)
        return text.strip()
    except:
        return "❌ Error decoding message."

def hide_text_in_image(image_path, secret_text, output_image):
    """Embed secret text into an image using LSB steganography."""
    img = cv2.imread(image_path)
    if img is None:
        return "❌ Error: Image file not found or format not supported. Use PNG."

    binary_text = text_to_binary(secret_text) + '1111111111111110'  # End delimiter

    data_index = 0
    total_pixels = img.shape[0] * img.shape[1] * 3  # Total available bits in image

    if len(binary_text) > total_pixels:
        return "❌ Error: Message too large for this image!"

    for row in img:
        for pixel in row:
            for i in range(3):  # Modify R, G, B LSB
                if data_index < len(binary_text):
                    pixel[i] = (pixel[i] & 0b11111110) | int(binary_text[data_index])
                    data_index += 1

    cv2.imwrite(output_image, img)
    return f"✅ Secret message hidden in {output_image}"

def extract_text_from_image(image_path):
    """Extract hidden text from an image using LSB steganography."""
    if not os.path.exists(image_path):
        return "❌ Error: Image file not found!"

    img = cv2.imread(image_path)
    if img is None:
        return "❌ Error: Unable to read the image file."

    binary_text = ""
    for row in img:
        for pixel in row:
            for i in range(3):  # Extract LSB from RGB
                binary_text += str(pixel[i] & 1)

                # Stop extraction when delimiter (1111111111111110) is detected
                if binary_text[-16:] == "1111111111111110":
                    return binary_to_text(binary_text[:-16])  # Remove delimiter before decoding

    return "❌ No hidden message found."
