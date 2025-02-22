import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('INATURALIST_API_TOKEN')

if not API_TOKEN:
    raise ValueError("API token not found. Check your .env file.")

INATURALIST_URL = "https://api.inaturalist.org/v1/computervision/score_image"

def test_api_connection():
    """Check if the iNaturalist API is reachable."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(INATURALIST_URL, headers=headers)

    if response.status_code == 200:
        print("✅ iNaturalist API is connected and working!")
    else:
        print(f"Failed to connect. Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_api_connection()
