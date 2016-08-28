import os

# ex :) API_GW_BACKEND_BASE_URL = 'http://localhost:8080'
API_GW_BASE_URL = os.environ.get('API_GW_BASE_URL') or 'http://localhost'

SERVICE_MOVIE_NAME = 'micromovie'
SERVICE_POLITICS_NAME = 'micropolitics'

SERVICE_MOVIE_RESOURCE = '/movies/'
SERVICE_POLITICS_RESOURCE = '/politics/bill/'
