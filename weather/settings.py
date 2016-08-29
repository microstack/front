import os

# ex :) API_GW_BACKEND_BASE_URL = 'http://localhost:8080'
API_GW_BASE_URL = os.environ.get('API_GW_BASE_URL') or 'http://localhost'
FRONT_WEATHER_PORT = os.environ.get('FRONT_WEATHER_PORT') or 5000
