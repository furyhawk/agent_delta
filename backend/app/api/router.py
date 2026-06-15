"""API router aggregation."""

from app.api.routes.v1 import v1_router

# Direct alias — avoids FastAPI 0.135+ validation that rejects routes with
# empty raw paths (e.g. @router.get("")) when include_router has no prefix.
# The prefix (settings.API_V1_STR) is applied in main.py.
api_router = v1_router
