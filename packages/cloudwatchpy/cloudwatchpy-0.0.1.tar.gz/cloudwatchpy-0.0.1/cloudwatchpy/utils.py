from pathlib import Path
import uuid
import os
from typing import Optional
from dotenv import load_dotenv


def generate_request_id() -> str:
    """Generate a unique request ID for tracing."""
    return str(uuid.uuid4())


def get_env_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    """Read environment variable with fallback to project .env file search."""
    
    # Step 1: Check direct system environment variable
    value = os.getenv(key)
    if value is not None:
        return value

    # Step 2: Try loading from root .env if not already loaded
    dotenv_loaded = False
    env_path = Path(".env")
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)
        dotenv_loaded = True

    # Step 3: Try to search for any .env file in the project directory
    if not dotenv_loaded:
        for root, dirs, files in os.walk(Path.cwd()):
            if ".env" in files:
                load_dotenv(dotenv_path=Path(root) / ".env")
                dotenv_loaded = True
                break

    # Step 4: After loading, check again
    value = os.getenv(key)
    if value is not None:
        return value

    # Step 5: If still not found, return default
    return default


def get_client_ip(headers: dict, fallback_ip: Optional[str] = None) -> Optional[str]:
    """Extract real client IP from headers (used in proxies, middlewares)."""
    x_forwarded_for = headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return fallback_ip
