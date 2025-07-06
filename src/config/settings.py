import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
XRAY_URL = os.getenv("XRAY_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
AUTH_HEADER = {
    "Authorization": f"Basic {os.getenv('AUTH_TOKEN')}",
    "Content-Type": "application/json"
}
