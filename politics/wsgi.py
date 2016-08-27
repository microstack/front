from views import app
from settings import FRONT_POLITICS_PORT

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FRONT_POLITICS_PORT)
