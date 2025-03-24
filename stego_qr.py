import qrcode
from PIL import Image

def generate_qr(message, output_path):
    """Generate a QR code from the message and save it to the given path."""
    qr = qrcode.make(message)
    qr.save(output_path)
    return f"QR Code saved successfully at {output_path}"

def decode_qr(image_path):
    """Decode a QR code and return the hidden message."""
    from pyzbar.pyzbar import decode
    img = Image.open(image_path)
    decoded_objects = decode(img)
    
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    else:
        return "No QR code found!"
