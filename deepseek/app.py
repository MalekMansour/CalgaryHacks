import cv2
import requests
import os
from dotenv import load_dotenv

# Ensure the .env file is loaded before accessing environment variables
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
    url = "https://api.deepseek.com/v1/recognize"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            return response.json()
    except requests.RequestException as e:
        print(f"Error sending image to DeepSeek API: {e}")
        return None

# Initialize the camera
cap = cv2.VideoCapture(0)

# Ensure the directory exists for saving images
output_dir = 'captured_images'
os.makedirs(output_dir, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Display the frame
    cv2.imshow('Camera', frame)

    # Check if 't' key is pressed to take a picture
    if cv2.waitKey(1) & 0xFF == ord('t'):
        image_path = os.path.join(output_dir, 'current_frame.jpg')
        cv2.imwrite(image_path, frame)
        print("Image captured and saved.")

        # Recognize the image
        result = recognize_image(image_path)
        
        if result:
            recognized_name = result.get('name', 'Unknown')
            print(f"Recognized Object: {recognized_name}")

            # Display the recognized name on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, recognized_name, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
