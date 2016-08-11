import os

# ex :) API_GW_BACKEND_BASE_URL = 'http://localhost:8080'
API_GW_BASE_URL = os.environ.get('API_GW_BASE_URL') or 'http://localhost'
FRONT_MAIN_PORT = os.environ.get('FRONT_MAIN_PORT') or 5000
FRONT_MOVIES_PORT = os.environ.get('FRONT_MOVIES_PORT') or 5000
