import os
import cv2
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env file
API_KEY = os.getenv('GOOGLE_CLOUD_VISION_API_KEY')
if not API_KEY:
    raise ValueError("API key not found. Please check the .env file and ensure 'GOOGLE_CLOUD_VISION_API_KEY' is set.")

# Google Cloud Vision API URL
VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

# Wildlife-related labels
WILDLIFE_CATEGORIES = {"animal", "plant", "tree", "bird", "mammal", "insect", "fish", "flower", "reptile", "amphibian"}

def recognize_image_google(image_path):
    """Send an image to Google Cloud Vision API for label detection."""
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Encode image data in base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    # Prepare the request payload
    payload = {
        "requests": [{
            "image": {"content": encoded_image},
            "features": [{"type": "LABEL_DETECTION", "maxResults": 5}]
        }]
    }

    # Send the request
    response = requests.post(VISION_URL, json=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return None

    return response.json()

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)  

    # Display the frame
    cv2.imshow('Camera', frame)

    # Check if 't' key is pressed to take a picture
    if cv2.waitKey(1) & 0xFF == ord('t'):
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        print("Image Captured")

        # Recognize the image
        result = recognize_image_google(image_path)
        
        if result:
            # Extract labels
            labels = result.get('responses', [{}])[0].get('labelAnnotations', [])
            recognized_labels = [label['description'].lower() for label in labels]
            
            # Check if the recognized labels belong to wildlife categories
            wildlife_labels = [label for label in recognized_labels if any(category in label for category in WILDLIFE_CATEGORIES)]

            if wildlife_labels:
                recognized_text = f"Wildlife Detected: {', '.join(wildlife_labels)}"
            else:
                recognized_text = "Not a wildlife"
        else:
            recognized_text = "Recognition failed"

        # Print result in terminal
        print(recognized_text)

        # Display recognized text on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, recognized_text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
