import os

from views import app

if __name__ == "__main__":
    host = os.environ.get('HOST')
    app.run(host=host)
