import os

environment = os.getenv("DJANGO_ENV", "local").strip().lower()

if environment == "production":
    from .production import *  # noqa: F401,F403
elif environment == "local":
    from .local import *  # noqa: F401,F403
else:
    from .base import *  # noqa: F401,F403
