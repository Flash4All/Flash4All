import requests
from decimal import Decimal
from flask import Blueprint, render_template, abort, jsonify, request
from redis_client import redis_client
import sys, os

arbitrage_routes = Blueprint('arbitrage', __name__)

token_list = requests.get('https://flash4all.net/api/tokens').json()
MARKETS=["uniswap", "kyber"]

@arbitrage_routes.route('', methods=["POST"])
def arbitrage_index():
    data = request.json
    token1 = data['token']

    for token2 in token_list:
        if token2 != token1:
            for token3 in token_list:
                if token3 != token1 and token3 != token2:
                    arbitriage_opps = calculate_forward(token1, token2, token3)
                    # arbitriage_opps.append(calculate_reversal(token1, token2, token3))
    arbitriage_opps.sort(reverse=True, key = get_tuple_calcutions)
    return jsonify(result=arbitriage_opps[:5])


def calculate_forward(token1, token2, token3=None):
   results = []
   trade_1 = None
   trade_2 = None
   trade_3 = None
   for first_trade_market in MARKETS:
       trade_1 = redis_client.get(f'{first_trade_market},{token1},{token2}').decode().split(',')
       for second_trade_market in MARKETS:
           if token3 is None: 
               trade_2 = redis_client.get(f'{second_trade_market},{token2},{token1}').decode().split(',')
               forward_calculation = ((Decimal(trade_1[0])) * (1 / Decimal(trade_2[1])) ) - 1
               forward_calculation_percent = forward_calculation * 100
               results.append((f'{first_trade_market},{second_trade_market},{token1},{token2}', forward_calculation_percent))
           for third_trade_market in MARKETS:
               try:
                   if token3 is not None:
                       trade_2 = redis_client.get(f'{second_trade_market},{token3},{token2}').decode().split(',')
                       trade_3 = redis_client.get(f'{third_trade_market},{token1},{token3}').decode().split(',')
                       forward_calculation = ((Decimal(trade_1[0])) * (1 / Decimal(trade_2[1])) * (1 / Decimal(trade_3[1]))) - 1
                       forward_calculation_percent = forward_calculation * 100
                       results.append((f'{first_trade_market},{second_trade_market},{third_trade_market},{token1},{token2},{token3}', forward_calculation_percent))
               except Exception as e:
                   print(first_trade_market, second_trade_market, third_trade_market)
                   print(f'TOKENS: {token1}, {token2}, {token3}')
                   print(f'TRADES: {trade_1}, {trade_2}, {trade_3}')
                   exc_type, exc_obj, exc_tb = sys.exc_info()
                   fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                   print(exc_type, fname, exc_tb.tb_lineno)
                   print('__________________________')
   return results

def calculate_reversal(token1, token2, token3):
    pass
    # try:
    #     trade_1 = redis_client.get(f'{market},{token1},{token2}').decode().split(',')
    #     trade_2 = redis_client.get(f'{market},{token3},{token2}').decode().split(',')
    #     trade_3 = redis_client.get(f'{market},{token1},{token3}').decode().split(',')
    #     reversal_calculation = (1 / (Decimal(trade_1[1])) * (Decimal(trade_2[0])) * (Decimal(trade_3[0]))) - 1
    #     reversal_calculation_percent = reversal_calculation * 100
    #     return f'{token1},{token2},{token3}', reversal_calculation_percent
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    #     return {'error': str(e)}
    #

def get_tuple_calcutions(item):
    print(item)
    return item[1]
