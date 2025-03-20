import logging

logging.basicConfig(filename="steganography.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log security events."""
    logging.info(message)
