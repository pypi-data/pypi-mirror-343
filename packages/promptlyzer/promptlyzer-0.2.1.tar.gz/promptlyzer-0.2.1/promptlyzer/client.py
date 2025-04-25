import os
import json
import requests
import time
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta

from .exceptions import (
    PromptlyzerError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    ServerError,
    RateLimitError
)


class PromptlyzerClient:
    """
    Client for fetching prompts from the Promptlyzer API with caching capabilities,
    connection pooling, and asynchronous request support.
    """
    
    def __init__(
        self,
        api_url: str = None,
        email: str = None,
        password: str = None,
        token: str = None,
        environment: str = "dev",
        cache_ttl_minutes: int = 5,
        max_pool_connections: int = 10
    ):
        """
        Initialize a new PromptlyzerClient.
        
        Args:
            api_url: The URL of the Promptlyzer API.
            email: The email for authentication.
            password: The password for authentication.
            token: An existing auth token (if available).
            environment: The prompt environment to use (dev, staging, prod).
            cache_ttl_minutes: Cache time-to-live in minutes. Defaults to 5 minutes.
            max_pool_connections: Maximum number of connections in the pool. Defaults to 10.
        """
        self.api_url = api_url or os.environ.get("PROMPTLYZER_API_URL", "http://localhost:8000")
        self.email = email or os.environ.get("PROMPTLYZER_EMAIL")
        self.password = password or os.environ.get("PROMPTLYZER_PASSWORD")
        self.token = token or os.environ.get("PROMPTLYZER_TOKEN")
        self.environment = environment
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self.max_pool_connections = max_pool_connections
        
        # Initialize cache
        self._cache = {}
        
        # Initialize session for connection pooling
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=self.max_pool_connections, 
                                              pool_maxsize=self.max_pool_connections)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        
        # Async session (initialized on demand)
        self._async_session = None
        
        # If token is not provided but email and password are,
        # authenticate automatically
        if not self.token and self.email and self.password:
            self.authenticate()
    
    def __del__(self):
        """Cleanup resources on deletion."""
        if hasattr(self, '_session') and self._session:
            self._session.close()
    
    def authenticate(self) -> str:
        """
        Authenticate with the Promptlyzer API and get an access token.
        
        Returns:
            str: The access token.
        
        Raises:
            AuthenticationError: If authentication fails.
        """
        if not self.email or not self.password:
            raise AuthenticationError("Email and password must be provided for authentication")
        
        url = f"{self.api_url}/auth/login"
        payload = {
            "email": self.email,
            "password": self.password
        }
        
        try:
            response = self._session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            
            if not self.token:
                raise AuthenticationError("No access token returned from server")
            
            return self.token
        
        except requests.HTTPError as e:
            response = e.response
            if response.status_code == 401:
                raise AuthenticationError("Invalid email or password") from e
            self._handle_request_error(e, response)
    
    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests.
        
        Returns:
            Dict[str, str]: The headers with authentication token.
        
        Raises:
            AuthenticationError: If no token is available.
        """
        if not self.token:
            raise AuthenticationError("No authentication token available. Call authenticate() first.")
        
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def _get_cache_key(self, *args) -> str:
        """
        Generate a cache key from the arguments.
        
        Args:
            *args: Arguments to include in the cache key.
            
        Returns:
            str: The cache key.
        """
        return ":".join(str(arg) for arg in args)
    
    def _get_from_cache(self, cache_key: str) -> Tuple[bool, Any]:
        """
        Try to get a value from the cache.
        
        Args:
            cache_key: The cache key.
            
        Returns:
            Tuple[bool, Any]: A tuple of (is_cached, value).
                If is_cached is False, value will be None.
        """
        if cache_key not in self._cache:
            return False, None
            
        cached_item = self._cache[cache_key]
        if datetime.now() - cached_item["timestamp"] > self.cache_ttl:
            # Cache expired
            return False, None
            
        return True, cached_item["value"]
    
    def _add_to_cache(self, cache_key: str, value: Any) -> None:
        """
        Add a value to the cache.
        
        Args:
            cache_key: The cache key.
            value: The value to cache.
        """
        self._cache[cache_key] = {
            "value": value,
            "timestamp": datetime.now()
        }
    
    def list_prompts(self, project_id: str, environment: Optional[str] = None, use_cache: bool = True) -> Dict[str, Any]:
        """
        List all prompts in a project, returning only their latest versions.
        
        Args:
            project_id: The ID of the project.
            environment: The environment to filter by. Defaults to client's environment.
            use_cache: Whether to use cached results if available. Defaults to True.
            
        Returns:
            Dict[str, Any]: An object containing prompts and total count.
        """
        env = environment or self.environment
        cache_key = self._get_cache_key("list_prompts", project_id, env)
        
        if use_cache:
            is_cached, cached_value = self._get_from_cache(cache_key)
            if is_cached:
                return cached_value
        
        url = f"{self.api_url}/projects/{project_id}/prompts?env={env}"
        headers = self.get_headers()
        
        response = self._make_request("GET", url, headers=headers)
        
        self._add_to_cache(cache_key, response)
        
        return response
    
    def get_prompt(self, project_id: str, prompt_name: str, environment: Optional[str] = None, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get a specific prompt by name, returning only the latest version.
        
        Args:
            project_id: The ID of the project.
            prompt_name: The name of the prompt.
            environment: The environment to get the prompt from. Defaults to client's environment.
            use_cache: Whether to use cached results if available. Defaults to True.
            
        Returns:
            Dict[str, Any]: The prompt object with the latest version.
        """
        env = environment or self.environment
        cache_key = self._get_cache_key("get_prompt", project_id, prompt_name, env)
        
        if use_cache:
            is_cached, cached_value = self._get_from_cache(cache_key)
            if is_cached:
                return cached_value
        
        url = f"{self.api_url}/projects/{project_id}/prompts/{prompt_name}?env={env}"
        headers = self.get_headers()
        
        response = self._make_request("GET", url, headers=headers)
        
        self._add_to_cache(cache_key, response)
        
        return response
    
    def clear_cache(self) -> None:
        """
        Clear the entire cache.
        """
        self._cache = {}
    
    def clear_prompt_cache(self, project_id: str, prompt_name: str = None, environment: Optional[str] = None) -> None:
        """
        Clear cache for a specific prompt or all prompts in a project.
        
        Args:
            project_id: The ID of the project.
            prompt_name: The name of the prompt. If None, clear all prompts in the project.
            environment: The environment to clear. If None, clear client's environment.
        """
        env = environment or self.environment
        
        if prompt_name:
            get_key = self._get_cache_key("get_prompt", project_id, prompt_name, env)
            if get_key in self._cache:
                del self._cache[get_key]
        else:
            list_key = self._get_cache_key("list_prompts", project_id, env)
            if list_key in self._cache:
                del self._cache[list_key]
            
            keys_to_delete = []
            for key in self._cache:
                if project_id in key and env in key:
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del self._cache[key]
    
    def _make_request(self, method: str, url: str, headers: Dict[str, str] = None, json_data: Dict[str, Any] = None) -> Any:
        """
        Make a request to the Promptlyzer API using connection pooling.
        
        Args:
            method: The HTTP method to use.
            url: The URL to request.
            headers: The headers to include.
            json_data: The JSON data to send.
            
        Returns:
            Any: The parsed JSON response.
            
        Raises:
            Various PromptlyzerError subclasses depending on the error.
        """
        try:
            response = self._session.request(method, url, headers=headers, json=json_data)
            response.raise_for_status()
            return response.json()
        
        except requests.HTTPError as e:
            return self._handle_request_error(e, e.response)
    
    def _handle_request_error(self, error: requests.HTTPError, response: requests.Response) -> None:
        """
        Handle HTTP errors from the API.
        
        Args:
            error: The HTTPError exception.
            response: The response object.
            
        Raises:
            AuthenticationError: For 401 status codes.
            ResourceNotFoundError: For 404 status codes.
            ValidationError: For 400 and 422 status codes.
            RateLimitError: For 429 status codes.
            ServerError: For 500+ status codes.
            PromptlyzerError: For all other error codes.
        """
        status_code = response.status_code
        
        try:
            error_data = response.json()
            detail = error_data.get("detail", "Unknown error")
        except (ValueError, KeyError):
            detail = response.text or "Unknown error"
        
        if status_code == 401:
            raise AuthenticationError(detail, status_code, response)
        elif status_code == 404:
            raise ResourceNotFoundError(detail, status_code, response)
        elif status_code in (400, 422):
            raise ValidationError(detail, status_code, response)
        elif status_code == 429:
            raise RateLimitError(detail, status_code, response)
        elif status_code >= 500:
            raise ServerError(detail, status_code, response)
        else:
            raise PromptlyzerError(detail, status_code, response)