import socket
from config import Config


class ProductConfig(Config):
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 80
    DEBUG = False

    RUN_SETTING = dict(Config.RUN_SETTING, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })
    Config.SWAGGER['host'] = '{}.{}'.format(HOST, PORT)
