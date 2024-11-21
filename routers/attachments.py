from fastapi import HTTPException, APIRouter
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
router = APIRouter()
load_dotenv()

# Load Cloudflare credentials from environment variables
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
print(CLOUDFLARE_ACCOUNT_ID)

@router.post("/get-upload-url/")
def get_upload_url():
    """
    Generate and return a Cloudflare Direct Creator Upload URL
    """
    # Cloudflare API endpoint to create a direct upload URL
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/images/v2/direct_upload"
    
    # Headers for the request
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"
    }

    # Send request to Cloudflare API
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        # Return the upload URL to the frontend
        result = response.json()["result"]
        return {
            "uploadURL": result["uploadURL"],
            "imageID": result["id"]
        }
    else:
        # Handle errors
        raise HTTPException(status_code=response.status_code, detail=response.json())

