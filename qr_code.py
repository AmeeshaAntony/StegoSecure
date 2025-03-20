import os
import cv2
import qrcode
from pyzbar.pyzbar import decode

def generate_qr():
    """Ask for an image path first, then generate a QR code with a secret message."""
    output_qr = input("Enter the QR image path to save (e.g., my_qr.png): ")

    # Ensure file extension is .png
    if not output_qr.lower().endswith(".png"):
        output_qr += ".png"

    message = input("Enter the secret message to hide in QR: ")

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(output_qr)

    return f"✅ QR code saved as {output_qr}"

def decode_qr(qr_path):
    """Decode the message from an existing QR image."""
    if not os.path.exists(qr_path):
        return "❌ Error: QR code file not found."

    img = cv2.imread(qr_path)
    if img is None:
        return "❌ Error: Unable to load the image. Make sure it's a valid QR code image."

    decoded_objects = decode(img)
    if not decoded_objects:
        return "❌ No QR code detected in the image."

    return f"{decoded_objects[0].data.decode('utf-8')}"
