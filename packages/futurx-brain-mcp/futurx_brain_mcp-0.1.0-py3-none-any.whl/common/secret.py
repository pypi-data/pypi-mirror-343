import os

API_KEY = os.getenv("FUTURX_BRAIN_API_KEY") or ""
BASE_URL = os.getenv("FUTURX_BRAIN_BASE_URL") or "http://localhost:8081"
# TODO: get host id from the api key
HOST_ID = os.getenv("FUTURX_BRAIN_HOST_ID") or ""