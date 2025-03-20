import cv2
from deepface import DeepFace

def authenticate_face(image_path, reference_image="face.jpg", threshold=0.4):
    """Authenticate using facial recognition with error handling and preprocessing."""
    try:
        # Load and convert both images to RGB format
        img1 = cv2.imread(image_path)
        img2 = cv2.imread(reference_image)

        if img1 is None or img2 is None:
            return "❌ Error: One or both images not found or unreadable."

        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        # Perform face verification
        result = DeepFace.verify(img1, img2, model_name="Facenet", distance_metric="cosine")

        # Compare with threshold
        if result["verified"] or result["distance"] < threshold:
            return f"✅ Face Authentication Successful! (Distance: {result['distance']:.4f})"
        else:
            return f"❌ Face Authentication Failed! (Distance: {result['distance']:.4f})"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
