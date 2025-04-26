import os

# Constants for the base URLs
ACTUALIZATION_BASE_URL = "https://actualization.ai"  # website url
LOCALHOST_BASE_URL = "http://127.0.0.1:3000"  # website local host

# Constants for API endpoints
GAUNTLET_API_BASE_URL = "http://gauntlet-load-balancer-203818527.us-east-1.elb.amazonaws.com"  # gauntlet load balancer
LOCALHOST_API_BASE_URL = "http://127.0.0.1:8000"  # gauntlet local host


def get_report_url(request_id: str) -> str:
    """
    Returns the appropriate report URL based on environment variables.

    Args:
        request_id: The request ID to be included in the URL

    Returns:
        The full URL to the report, using localhost if mr_robot is set
    """
    base_url = (
        LOCALHOST_BASE_URL
        if os.getenv("mr_robot") == "development"
        else ACTUALIZATION_BASE_URL
    )
    return f"{base_url}/request/{request_id}"


def get_api_endpoint(endpoint_path: str) -> str:
    """
    Returns the appropriate API endpoint URL based on environment variables.

    Args:
        endpoint_path: The specific endpoint path (e.g., "self_harm_trial")

    Returns:
        The full URL to the API endpoint, using localhost if mr_robot is set
    """
    base_url = (
        LOCALHOST_API_BASE_URL
        if os.getenv("mr_robot") == "development"
        else GAUNTLET_API_BASE_URL
    )
    return f"{base_url}/{endpoint_path}"
