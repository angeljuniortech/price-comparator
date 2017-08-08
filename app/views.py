#-*- coding:UTF-8 -*-

from flask import request

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from flask_restful import Resource
from requests import Session
from requests.packages import urllib3

from constants import *
from utils import *


class MainView(Resource):
    
    def get(self):
        
        context = {
            'version': 0.1,
        }
        return render_to_json(context)


class PingView(Resource):
    
    def get(self):

        context = {
            'message': 'pong',
            'version': 0.1,
        }
        return render_to_json(context)


class OffersView(Resource):

    def get(self):

        urllib3.disable_warnings()
        session = Session()
        sessionHeaders = {
            'Host': 'www.wong.com.pe',
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        response = session.get(
            "https://www.wong.com.pe/pe/supermercado/login.html",
            headers = sessionHeaders,
        )
        sessionHeaders = {
            'Host': 'spreadsheets.google.com',
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': "application/x-www-form-urlencoded",
            'Referer': "https://www.wong.com.pe/pe/supermercado/login.html",
            'Origin': "https://www.wong.com.pe",
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        response = session.get(
            "https://spreadsheets.google.com/feeds/list/1XEafTjhpr00UIlJEigki2d_e65ejrcLguVcYdMB3NKc/4/public/values?alt=json",
            headers = sessionHeaders,
        )
        page = response.json()["feed"]["entry"]
        items = []
        for raw in page:
            items.append({
                "name": u"%s" % raw["gsx$title"]["$t"],
                "description": u"%s, %s, %s" % (raw["gsx$title"]["$t"], raw["gsx$marca"]["$t"], raw["gsx$desc"]["$t"]),
                "price": raw["gsx$antes"]["$t"],
                "offer": raw["gsx$ahora"]["$t"],
                "alternativesInMarket": []
            })
        for item in items:
            try:
                marketRaw = session.get("http://0.0.0.0:5000/market/", params = {"pName": item["description"]})
                marketPageRaw = marketRaw.json()
                item["alternativesInMarket"] = marketPageRaw
            except:
                pass
        return render_to_json(items, 200)


class MarketView(Resource):

    def get(self):

        pName = request.args.get('pName', '')
        pID = get_product_by_name(pName)
        if pID == "":
            context = {
            }
            return render_to_json(context, 200)
        nowDate = datetime.utcnow()
        nowYesterday = nowDate - timedelta(days = 1)
        urllib3.disable_warnings()
        session = Session()
        sessionHeaders = {
            'Host': 'sistemas.minag.gob.pe',
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://sistemas.minag.gob.pe/sisap/portal2/ciudades/',
            'Cookie': 'autentificator=6529fchilvqrig9p6l8l20rfg1',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        sessionParams = {
            "region": "150000", # Lima
            "variables[]": "min_precio_min",
            "fecha": "%s" % nowYesterday.strftime("%d/%m/%Y"),
            "anios[]": "%s" % nowYesterday.strftime("%Y"),
            "meses[]": "%s" % nowYesterday.strftime("%m"),
            "productos[]": "%s" % pID,
            "periodicidad": "dia",
            "__ajax_carga_final": "consulta",
            "ajax": "true",
        }
        response = session.get(
            "http://sistemas.minag.gob.pe/sisap/portal2/ciudades/resumenes/filtrar",
            headers = sessionHeaders,
            params = sessionParams,
        )
        page = BeautifulSoup(response.text, "lxml")
        items = []
        for raw in page.find("table").find_all("tr", class_ = "contenido"):
            if raw.find_all("td")[3].text != "":
                items.append({
                    "description": "%s" % raw.find_all("td")[0].text,
                    "unitMetric": "%s" % raw.find_all("td")[1].text,
                    "quantity": "%s" % raw.find_all("td")[2].text,
                    "price": Decimal(raw.find_all("td")[3].text),
                })
        return render_to_json(items, 200)
