import requests
from decimal import Decimal
from flask import Blueprint, render_template, abort, jsonify, request
from redis_client import redis_client

arbitrage_routes = Blueprint('arbitrage', __name__)

token_list = requests.get('https://flash4all.net/api/tokens').json()

@arbitrage_routes.route('', methods=["POST"])
def arbitrage_index():
    data = request.json
    token1 = data['token']
    arbitriage_opps = []

    for token2 in token_list:
        if token2 != token1:
            for token3 in token_list:
                if token3 != token1 and token3 != token2:
                    print(token3, token2)
                    arbitriage_opps.append(calculate_forward(token1, token2, token3))
    arbitriage_opps.sort(reverse=True, key = get_tuple_calcutions)
    return jsonify(result=arbitriage_opps[:3])


def calculate_forward(token1, token2, token3):
    trade_1 = redis_client.get(f'{token1},{token2}').decode().split(',')
    trade_2 = redis_client.get(f'{token3},{token2}').decode().split(',')
    trade_3 = redis_client.get(f'{token1},{token3}').decode().split(',')
    forward_calculation = ((Decimal(trade_1[0])) * (1/Decimal(trade_2[1])) * (1/Decimal(trade_3[1])))-1
    forward_calculation_percent = forward_calculation * 100
    return (f'{token1},{token2},{token3}', forward_calculation_percent)

def get_tuple_calcutions(item):
    return item[1]

