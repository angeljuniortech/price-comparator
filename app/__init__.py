#-*- coding:UTF-8 -*-

from flask import jsonify
from flask import Flask
from flask_restful import Api
from flask_restful import Resource

from settings import *
from utils import render_to_json


app = Flask(__name__)
app.config.from_object('settings')

api = Api(app)


@app.after_request
def after_request(response):
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.errorhandler(404)
def view404(error):
    
    context = {
    }
    return render_to_json(context, 404)


@app.errorhandler(500)
def view500(error):
    
    context = {
    }
    return render_to_json(context, 500)


## URLs

from .views import MainView
from .views import PingView
from .views import OffersView
from .views import MarketView

api.add_resource(MainView	, '/')
api.add_resource(PingView	, '/ping/')
api.add_resource(OffersView	, '/offers/')
api.add_resource(MarketView	, '/market/')
