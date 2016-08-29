from views import app
from settings import FRONT_WEATHER_PORT

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FRONT_WEATHER_PORT)
