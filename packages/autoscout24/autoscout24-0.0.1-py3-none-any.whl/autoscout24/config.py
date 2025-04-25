import os
import dotenv
from pathlib import Path

# Determine project root and .env path relative to this file's location after install
# This might need adjustment depending on the final package structure
_CONFIG_DIR = Path(__file__).resolve().parent
# Assuming the intended project root is several levels up from the installed package source
# This is a common pattern but might need adjustment based on usage context
_PROJECT_ROOT_GUESS = _CONFIG_DIR.parent.parent.parent
env_path = _PROJECT_ROOT_GUESS / '.env'

# Load .env file if it exists, allowing environment variables to override
dotenv.load_dotenv(dotenv_path=env_path)

# Get API URL from environment or use default
# Use a distinct env var name to avoid conflicts if multiple clients are used
_PACKAGE_NAME_UPPER = "autoscout24".upper()
_ENV_VAR_NAME = f"{_PACKAGE_NAME_UPPER}_API_URL"
DEFAULT_BASE_URL = "https://api.carapis.com"  # Default API endpoint

BASE_URL = os.getenv(_ENV_VAR_NAME, DEFAULT_BASE_URL)

# You could add other package-level configurations here if needed
# print(f"Debug: Using {_ENV_VAR_NAME}={BASE_URL}") # Uncomment for debugging
