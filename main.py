import os
from encryption import decrypt_message
import image_stego
import audio_stego
import qr_code
import face_auth
import time_lock
import blockchain

def main():
    while True:
        print("\n🔹 Steganography & Security System 🔹")
        print("1️⃣ Hide Message in Image")
        print("2️⃣ Extract Message from Image")
        print("3️⃣ Hide Message in Audio")
        print("4️⃣ Extract Message from Audio")
        print("5️⃣ Generate QR Code")
        print("6️⃣ Decode QR Code")
        print("7️⃣ Face Authentication")
        print("9️⃣ Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            image_path = input("Enter image path: ")
            if not os.path.exists(image_path):
                print("❌ Error: Image file not found.")
                continue
            message = input("Enter secret message: ")
            output_image = input("Enter output image name (e.g., stego_image.png): ")
            print(image_stego.hide_text_in_image(image_path, message, output_image))

        elif choice == "2":
            image_path = input("Enter the stego image path: ")

            if not os.path.exists(image_path):
                print("❌ Error: File not found!")
            else:
                extracted_message = image_stego.extract_text_from_image(image_path)

                if extracted_message and extracted_message.strip():
                    decrypt_option = input("Is this an encrypted message? (yes/no): ").lower()
                    if decrypt_option == "yes":
                        try:
                            extracted_message = decrypt_message(extracted_message)
                        except Exception as e:
                            print(f"❌ Decryption failed: {e}")
                            extracted_message = "⚠️ Encrypted message but wrong key!"
            
                    print(f"🔓 Extracted Message: {extracted_message}")
                else:
                    print("❌ No hidden message found or extraction failed!")

        elif choice == "3":
            audio_path = input("Enter WAV file path: ")
            if not os.path.exists(audio_path):
                print("❌ Error: Audio file not found.")
                continue
            message = input("Enter secret message: ")
            output_audio = input("Enter output audio file name (e.g., stego_audio.wav): ")
            print(audio_stego.hide_text_in_audio(audio_path, message, output_audio))

        elif choice == "4":
            extracted_message = audio_stego.extract_text_from_audio("stego_audio.wav")
            decrypt_option = input("Is this an encrypted message? (yes/no): ").lower()
            if decrypt_option == "yes":
                extracted_message = decrypt_message(extracted_message)
            print(f"🔓 Extracted Message: {extracted_message}")

        elif choice == "5":
            message = input("Enter secret message: ")
            output_qr = input("Enter output QR image name (e.g., qr_code.png): ")
            print(qr_code.generate_qr(message, output_qr))

        elif choice == "6":
            qr_path = input("Enter QR code image path: ")
            if not os.path.exists(qr_path):
                print("❌ Error: QR code file not found.")
                continue
            print("🔓 Decoded Message:", qr_code.decode_qr(qr_path))

        elif choice == "7":
            face_image = input("Enter face image path for authentication: ")
            if not os.path.exists(face_image):
                print("❌ Error: Face image not found.")
                continue
            print(face_auth.authenticate_face(face_image))

        elif choice == "8":
            logs = blockchain.blockchain.get_logs()
            if logs and logs != ["❌ No logs found."]:
                print("\n📜 Blockchain Logs:")
                for log in logs:
                    print(f"📝 {log}")
            else:
                print("❌ No logs found.")

        elif choice == "9":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
