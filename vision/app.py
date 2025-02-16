import os
import cv2
import requests
from dotenv import load_dotenv

# Load API token
load_dotenv()
API_TOKEN = os.getenv('INATURALIST_API_TOKEN')

if not API_TOKEN:
    raise ValueError("API token not found. Check your .env file.")

# Correct iNaturalist API endpoint
INATURALIST_URL = "https://api.inaturalist.org/v1/computervision/score_image"

def recognize_image_inaturalist(image_path):
    """Send an image to iNaturalist for species recognition."""
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        # Make the request
        response = requests.post(INATURALIST_URL, headers=headers, files=files)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return "Wildlife not in our registry"

    # Extract results
    results = response.json().get("results", [])
    if not results:
        return "Wildlife not in our registry"

    # Get species names
    taxon = results[0].get("taxon", {})
    common_name = taxon.get("preferred_common_name", "Unknown")
    scientific_name = taxon.get("name", "Unknown")

    return f"{common_name} ({scientific_name})"

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        print("Image Captured")

        # Recognize image
        recognized_text = recognize_image_inaturalist(image_path)
        print(recognized_text)

        # Display result
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, recognized_text, (10, 30), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
