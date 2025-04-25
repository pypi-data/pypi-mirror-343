class PromptlyzerError(Exception):
    """Base exception for Promptlyzer client errors."""
    def __init__(self, message=None, http_status=None, response=None):
        self.message = message
        self.http_status = http_status
        self.response = response
        super().__init__(self.message)


class AuthenticationError(PromptlyzerError):
    """Exception raised for authentication errors."""
    pass


class ResourceNotFoundError(PromptlyzerError):
    """Exception raised when requested resource is not found."""
    pass


class ValidationError(PromptlyzerError):
    """Exception raised for validation errors."""
    pass


class ServerError(PromptlyzerError):
    """Exception raised for server errors."""
    pass


class RateLimitError(PromptlyzerError):
    """Exception raised when rate limit is exceeded."""
    pass