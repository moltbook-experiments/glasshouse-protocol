import requests
import logging
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all simulation agents with API client and authentication."""

    def __init__(self, agent_id: str, api_token: str, base_url: str = "http://127.0.0.1:8000"):
        self.agent_id = agent_id
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-Moltbook-Identity': self.api_token,  # Use Moltbook identity header
            'Content-Type': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None, max_retries: int = 3) -> requests.Response:
        """Make an authenticated API request with retry logic."""
        for attempt in range(max_retries):
            try:
                url = f"{self.base_url}{endpoint}"
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params)
                elif method.upper() == 'POST':
                    response = self.session.post(url, json=data, params=params)
                elif method.upper() == 'PUT':
                    response = self.session.put(url, json=data, params=params)
                elif method.upper() == 'DELETE':
                    response = self.session.delete(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                logger.info(f"API {method} {endpoint} - Status: {response.status_code}")
                return response

            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"API request failed (attempt {attempt + 1}/{max_retries}): {method} {endpoint} - {e}. Retrying in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    logger.error(f"API request failed after {max_retries} attempts: {method} {endpoint} - {e}")
                    raise

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a GET request."""
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a POST request."""
        return self._make_request('POST', endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a PUT request."""
        return self._make_request('PUT', endpoint, data=data)

    def delete(self, endpoint: str) -> requests.Response:
        """Make a DELETE request."""
        return self._make_request('DELETE', endpoint)