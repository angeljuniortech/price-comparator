#-*- coding:UTF-8 -*-

from os import environ as environment

from app import app
from settings import *


if __name__ == "__main__":
    
    port = int(environment.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port, debug = DEBUG, threaded = True)
