# -*- coding:utf-8 -*-

from flask import jsonify

from constants import *


def render_to_json(context, status = 200):
    
    response = jsonify(context)
    response.status_code = status
    return response


def get_product_by_name(name):
    
    productsName = name.split(" ")
    productID = ""
    for productName in productsName:
        for MARKET__PRODUCT__ID in MARKET__PRODUCTS:
            if productName.lower() == MARKET__PRODUCTS[MARKET__PRODUCT__ID].lower():
                productID = MARKET__PRODUCT__ID
    return productID

