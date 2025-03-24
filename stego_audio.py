import wave

def hide_text_in_audio(audio_path, secret_text, output_audio):
    """Embed secret text inside an audio file using LSB steganography."""
    song = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    binary_text = ''.join(format(ord(char), '08b') for char in secret_text) + '1111111111111110'

    for i in range(len(binary_text)):
        frame_bytes[i] = (frame_bytes[i] & 0b11111110) | int(binary_text[i])

    new_audio = wave.open(output_audio, 'wb')
    new_audio.setparams(song.getparams())
    new_audio.writeframes(frame_bytes)
    new_audio.close()
    song.close()

    return f"✅ Secret message hidden in {output_audio}"

def binary_to_text(binary):
    """Convert binary string to text correctly."""
    try:
        text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return text.encode('latin-1').decode('utf-8', 'ignore')  # Handle encoding issues
    except:
        return "❌ Error decoding message."

def extract_text_from_audio(audio_path):
    """Extract hidden text from an audio file."""
    song = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    binary_text = ""
    for byte in frame_bytes:
        binary_text += str(byte & 1)
        if binary_text[-16:] == "1111111111111110":  # Stop delimiter
            return binary_to_text(binary_text[:-16])

    return "❌ No hidden message found."



