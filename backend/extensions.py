"""
Shared Flask extensions.

The in-memory rate-limit store is suitable for local development.
Use a shared store such as Redis in a production deployment.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://"
)
