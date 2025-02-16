import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API token from the environment variable
API_TOKEN = os.getenv('INATURALIST_API_TOKEN')

if not API_TOKEN:
    raise ValueError("API token not found. Please check the .env file and ensure 'INATURALIST_API_TOKEN' is set.")

# iNaturalist API URL
INATURALIST_URL = "https://api.inaturalist.org/v1/observations"

# Send a test request to iNaturalist API
params = {
    'api_token': API_TOKEN,
    'per_page': 1  # Just retrieve one result to test
}

response = requests.get(INATURALIST_URL, params=params)

if response.status_code == 200:
    print("Authentication successful!")
else:
    print(f"Authentication failed: {response.status_code}, {response.text}")
