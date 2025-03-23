import cv2
import numpy as np

def hide_text_in_image(image_path, secret_text, output_image):
    img = cv2.imread(image_path)
    binary_text = ''.join(format(ord(char), '08b') for char in secret_text) + '1111111111111110'

    data_index = 0
    for row in img:
        for pixel in row:
            for i in range(3):  
                if data_index < len(binary_text):
                    pixel[i] = (pixel[i] & 0b11111110) | int(binary_text[data_index])
                    data_index += 1

    cv2.imwrite(output_image, img)
    return f"✅ Secret message hidden in {output_image}"

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    binary_text = ""
    for row in img:
        for pixel in row:
            for i in range(3):  
                binary_text += str(pixel[i] & 1)
                if binary_text[-16:] == "1111111111111110":
                    return ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text)-16, 8))
    return "❌ No hidden message found."
