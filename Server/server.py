import os

from app import create_app

from config.dev import DevConfig
from config.product import ProductConfig


if __name__ == '__main__':
    app = create_app(ProductConfig)
    if 'SECRET_KEY' not in os.environ:
        print("SECRET_KEY is not existing")

    app.run(host='0.0.0.0', port=80, debug=False)
