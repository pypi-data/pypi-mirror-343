import requests
import os
from typing import Optional, Dict, Any
import sys

# Import configuration (e.g., BASE_URL) - Assumes config.py exists in the same directory
from .config import BASE_URL

# Determine the directory where this script is located - needed for version
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class CarapisClientError(Exception):
    """Custom exception for CarapisClient errors."""
    pass


class CarapisClient:
    """
    Simplified Python client for a Carapis API variant.
    Makes direct HTTP requests.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the client parser.

        Args:
            api_key: Your Carapis API key (optional). If not provided,
                     the client operates in free tier mode (limited access).
        """
        # Use BASE_URL from config, ensure no trailing slash
        self.base_url = BASE_URL.rstrip('/')
        self.api_key = api_key
        # Define the specific API path part using a placeholder
        # This placeholder will be replaced by the build script
        self.api_base_path = "/apix/autoscout24/v2"

        # Set headers
        self._headers = {
            "Accept": "application/json",
            # User agent needs package name and version, use placeholders
            "User-Agent": f"CarapisClientPython/autoscout24/{self._get_version()}"
        }
        if self.api_key:
            self._headers["Authorization"] = f"ApiKey {self.api_key}"
        else:
            print("Warning: No API key provided. Operating in limited free tier mode.")

    @staticmethod
    def _get_version() -> str:
        """Reads the version from __init__.py (relative to this file)."""
        try:
            # Assumes __init__.py is in the same directory as client.py
            init_path = os.path.join(_SCRIPT_DIR, '__init__.py')
            with open(init_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('__version__'):
                        local_dict = {}
                        exec(line, globals(), local_dict)
                        return local_dict.get('__version__', 'unknown')
        except Exception as e:
            print(f"Warning: Could not read version from {init_path}: {e}", file=sys.stderr)
        return 'unknown'

    def _request(self, method: str, relative_path: str,
                 query_params: Optional[Dict[str, Any]] = None,
                 json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper method to make requests."""
        # Ensure relative path starts with a slash
        if not relative_path.startswith('/'):
            relative_path = '/' + relative_path

        # Construct the full URL
        url = f"{self.base_url}{self.api_base_path}{relative_path}"

        # Filter out None values from query_params before sending
        actual_query_params = {k: v for k, v in query_params.items() if v is not None} if query_params else None

        try:
            response = requests.request(
                method,
                url,
                headers=self._headers,
                params=actual_query_params,
                json=json_data,
                timeout=30  # Standard timeout
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            # Handle cases where response might be empty (e.g., 204 No Content)
            if response.status_code == 204 or not response.content:
                return {}
            return response.json()
        except requests.exceptions.HTTPError as e:
            try:
                error_details = response.json()
            except requests.exceptions.JSONDecodeError:
                error_details = response.text
            raise CarapisClientError(f"HTTP error {response.status_code} for {method} {url}: {error_details}") from e
        except requests.exceptions.RequestException as e:
            raise CarapisClientError(f"Request failed for {method} {url}: {e}") from e
        except ValueError as e:  # Catches JSONDecodeError
            raise CarapisClientError(f"Failed to decode JSON response for {method} {url}: {e}") from e

    # --- Example Endpoint Methods --- >
    # Add specific methods for common operations as needed.

    def list_vehicles(self, limit: Optional[int] = None,
                      page: Optional[int] = None,
                      ordering: Optional[str] = None,
                      search: Optional[str] = None,
                      # Add other relevant filter parameters here based on typical use
                      min_price: Optional[int] = None,
                      max_price: Optional[int] = None,
                      min_year: Optional[int] = None,
                      max_year: Optional[int] = None,
                      min_mileage: Optional[int] = None,
                      max_mileage: Optional[int] = None,
                      manufacturer_slug: Optional[str] = None,
                      model_slug: Optional[str] = None,
                      fuel_type: Optional[str] = None,
                      transmission: Optional[str] = None,
                      body_type: Optional[str] = None,
                      color: Optional[str] = None,
                      ) -> Dict[str, Any]:
        """Lists vehicles with optional filtering and pagination."""
        params = locals()
        params.pop('self')
        # Filter out None values explicitly for clarity
        query_params = {k: v for k, v in params.items() if v is not None}
        return self._request('GET', '/vehicles/', query_params=query_params)

    def get_vehicle(self, vehicle_id: int) -> Dict[str, Any]:
        """Retrieves details for a specific vehicle by its ID."""
        if not isinstance(vehicle_id, int) or vehicle_id <= 0:
            raise ValueError("vehicle_id must be a positive integer")
        return self._request('GET', f'/vehicles/{vehicle_id}/')

    # --- Add other common methods as needed ---
    # e.g., list_manufacturers, get_manufacturer, etc.

    # Example: Method for a hypothetical 'stats' endpoint
    # def get_stats(self) -> Dict[str, Any]:
    #     """Retrieves general statistics."""
    #     return self._request('GET', '/stats/')
