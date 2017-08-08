#-*- coding:UTF-8 -*-

from os.path import dirname


##
## App
##

SERVER = 'price-comparator'
SECRET_KEY = '*i-l07*@ecs8l2=5ee9kdm7eudw9x*^4zhhb+^qx7auc(&t-z5'
BASE_DIR = dirname(__file__)
DEBUG = False
BUNDLE_ERRORS = True


##
## Admins
##

ADMINS = ['price-comparator@mailinator.com']


##
## Local settings
##

try:
    from local_settings import *
except ImportError:
    pass
