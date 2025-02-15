import cv2
import requests
import os
from dotenv import load_dotenv

# Ensure the .env file is loaded
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f".env file not found at path: {dotenv_path}")
# Load the API key from the .env file
API_KEY = os.getenv('DEEPSEEK_API_KEY')
if not API_KEY:
    raise ValueError("API key not found. Please check the .env file and ensure 'DEEPSEEK_API_KEY' is set.")

# Function to send image to DeepSeek API
def recognize_image(image_path):
    url = "https://api.deepseek.com/recognize"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    files = {
        "image": open(image_path, "rb")
    }
    response = requests.post(url, headers=headers, files=files)
    return response.json()

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display the frame
    cv2.imshow('Camera', frame)

    # Save the frame as an image
    image_path = 'current_frame.jpg'
    cv2.imwrite(image_path, frame)

    # Recognize the image
    result = recognize_image(image_path)
    print(result)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()