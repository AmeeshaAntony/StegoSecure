import time

def time_lock_message(secret_text, unlock_time):
    """Locks the message until a future timestamp."""
    current_time = int(time.time())
    if current_time < unlock_time:
        return f"⏳ Message locked! Try after {unlock_time - current_time} seconds."
    return f"🔓 Message: {secret_text}"
