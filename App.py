# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)


@app.route('/api/v1/cities', methods=['GET'])
def getCities():
    response = requests.get("http://bankiros.ru/site/cities")
    soup = BeautifulSoup(response.text)
    cities = soup.find_all('a', "cities")
    list = []
    for item in cities:
        list.append({"name": item.text, "href": re.match(r'^[^.]*',item.get("href")[6:]).group(0)})
    return jsonify(list)

@app.route('/api/v1/currency/<string:city>', methods=['GET'])
def getInf(city):
    url = "http://" + city + ".bankiros.ru/currency"
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    tableCurr = soup.find('tbody', "table-body")
    tr = tableCurr.findAll('tr')
    list = []
    map = {}
    addresses = []
    for item in tr:
        if item.get('class')[0] == 'productBank':
            map['addresses'] = addresses
            list.append(map)
            map = {}
            addresses = []
            map['name'] = item.contents[1].text
            map['usd_buy'] = item.contents[3].text
            map['usd_sell'] = item.contents[5].text
            map['euro_buy'] = item.contents[7].text
            map['euro_sell'] = item.contents[9].text
        else:
            address = item.find('p', 'address')
            if address:
                addresses.append(address.text)
    list = list[1:]
    return jsonify(list)

if __name__ == '__main__':
    app.run(port=8080)
