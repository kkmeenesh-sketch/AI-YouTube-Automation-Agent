"""
Base API Client for all external API integrations.

Provides common functionality for API requests with error handling,
rate limiting, and retry logic.
"""

import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import RATE_LIMIT_ENABLED, PROXIES, HTTPS_PROXY, HTTP_PROXY
from src.utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """Base API client with common functionality."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API
            api_key: API key for authentication
            headers: Additional headers
            timeout: Request timeout in seconds
            max_retries: Number of retries for failed requests
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize session with retry strategy
        self.session = self._create_session(max_retries)
        
        # Set default headers
        self.headers = headers or {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.headers["User-Agent"] = "AI-YouTube-Automation-Agent/1.0"
    
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST", "PUT"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set proxies if configured
        if PROXIES:
            session.proxies.update(PROXIES)
            logger.info(f"Using proxy: {HTTPS_PROXY or HTTP_PROXY}")
        
        return session
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments for requests
        
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        return self._request("GET", url, params=params, **kwargs)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make POST request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json: JSON body
            **kwargs: Additional arguments for requests
        
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        return self._request("POST", url, data=data, json=json, **kwargs)
    
    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Make PUT request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("PUT", url, data=data, json=json, **kwargs)
    
    def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """Make DELETE request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("DELETE", url, **kwargs)
    
    def _request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request with error handling.
        
        Args:
            method: HTTP method
            url: Full URL
            **kwargs: Arguments for requests
        
        Returns:
            Response object
        
        Raises:
            requests.RequestException: On request failure
        """
        try:
            kwargs.setdefault("timeout", self.timeout)
            kwargs.setdefault("headers", self.headers)
            
            logger.debug(f"{method} {url}")
            response = self.session.request(method, url, **kwargs)
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            logger.debug(f"Response status: {response.status_code}")
            return response
        
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def close(self):
        """Close session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
