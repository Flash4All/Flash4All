import requests
from decimal import Decimal
from flask import Blueprint, render_template, abort, jsonify, request

arbitrage_routes = Blueprint('arbitrage', __name__)

@arbitrage_routes.route('', methods=["POST"])
def arbitrage_index():
   if request.method == 'POST':
       data = request.json
       token1 = data['token1']
       token2 = data['token2']
       token3 = data['token3']

       forward, reverse = calculate_arbitrage(token1, token2, token3)
       return jsonify(forward=forward, reverse=reverse)


def calculate_arbitrage(token, token2, token3):
    #pair 1 of the triangle eth/dai
    bid_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount=1&dex=ag').json()
    ask_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount=1&dex=ag').json()

    #pair 2 of the triangle SAI/DAI
    bid_price2 = requests.get(f'https://api-v2.dex.ag/price?from={token3}&to={token2}&fromAmount=1&dex=ag').json()
    ask_price2 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token3}&fromAmount=1&dex=ag').json()

    #pair 3 of the triangle ETH/SAI
    bid_price3 = requests.get(f'https://api-v2.dex.ag/price?from={token3}&to={token}&fromAmount=1&dex=ag').json()
    ask_price3 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token3}&fromAmount=1&dex=ag').json()

    ask_1 = Decimal(ask_price1['price'].replace(',','.'))
    bid_1 = Decimal(bid_price1['price'].replace(',','.'))
    ask_2 = Decimal(ask_price2['price'].replace(',','.'))
    bid_2 = Decimal(bid_price2['price'].replace(',','.'))
    ask_3 = Decimal(ask_price3['price'].replace(',','.'))
    bid_3 = Decimal(bid_price3['price'].replace(',','.'))

    bid_pair_1 = 1/bid_1
    bid_pair_2 = 1/bid_2
    bid_pair_3 = 1/bid_3
    ask_pair_1 = ask_1
    ask_pair_2 = ask_2
    ask_pair_3 = ask_3

    forward_calculation = ((bid_pair_1 * (1/ask_pair_2) * (1/ask_pair_3)-1))
    forward_calculation_percent = forward_calculation * 100

    reversal_calculation = (bid_pair_3 * bid_pair_2 *(1/ask_pair_1) - 1)
    reversal_calculation_percent = reversal_calculation * 100
    return (forward_calculation, reversal_calculation)

