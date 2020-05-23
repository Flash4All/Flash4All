import requests
import sys
import os
from decimal import Decimal
import json
from redis_client import redis_client

#market_prices = requests.get(f'https://api.kyber.network/market')
tokenlist  = {
            'MKR',
            'DAI',
            'BAT',
            'TUSD',
            'USDT',
            'ETH',
            'USDC',
            'LINK',
            'ZRX',
            'KNC'
}


token_list = [t for t in tokenlist if t != "REP"]


#trade_path = input('Enter potential path')
([x for x in tokenlist])

#buying = ask price
#selling = bid price

def find_uniswap_bid_ask(token, token2):
    if token == 'SAI' or token2 == 'SAI' or token == 'USDT' or token2 == 'USDT' or token == 'OMG' or token2 == 'OMG':
        return

    dex_ = 'uniswap'
    initial_amount = 5
    try:
    #bid price = sell price
    # buy side = ask price should be lower
        uniswap_sell_side = requests.get(
        f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount={initial_amount}&dex={dex_}&limitAmount=').json()
        uniswap_buy_side = requests.get(
        f'https://api-v2.dex.ag/price?from={token2}&to={token}&toAmount={initial_amount}&dex={dex_}&limitAmount=').json()

        uniswap_bid_float = uniswap_sell_side.get('price')
        uniswap_ask_float = Decimal(uniswap_buy_side.get('price'))
        print(f'{token}->{token2}: Buy {uniswap_ask_float}, Sell {uniswap_bid_float}')
        redis_client.set(f'uniswap,{token},{token2}', f'{uniswap_bid_float}, {uniswap_ask_float}')
    except Exception as e:
        print(token, token2)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'error': str(e)}


def find_kyber_bid_ask(token, token2):
    if token == 'SAI' or token2 == 'SAI' or token == 'USDT' or token2 == 'USDT' or token == 'OMG' or token2 == 'OMG':
        return
    dex_ = 'kyber'
    initial_amount = 5
    print('______________')
    try:
        kyber_sell_side = requests.get(
            f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount={initial_amount}&dex={dex_}').json()
        kyber_buy_side = requests.get(
            f'https://api-v2.dex.ag/price?from={token2}&to={token}&toAmount={initial_amount}&dex={dex_}').json()

        kyber_bid_float = kyber_sell_side.get('price')
        kyber_ask_float = kyber_buy_side.get('price')

        print(f'{token}->{token2}: Buy {kyber_ask_float}, Sell {kyber_bid_float}')
        redis_client.set(f'kyber,{token},{token2}', f'{kyber_bid_float},{kyber_ask_float}')
    except Exception as e:
        print(e)

for token in token_list:
    [find_kyber_bid_ask(token, token2) for token2 in token_list if token != token2]
    [find_uniswap_bid_ask(token, token2) for token2 in token_list if token != token2]








"""
def find_kyber_bid_ask(token, token2):
    token_1_address = addresses[token]
    token_2_address = addresses[token2]
    try:
        buy_side = requests.get(f'https://api.kyber.network/quote_amount?base={token_1_address}&quote={token_2_address}&base_amount={5}&type=buy').json()
        sell_side = requests.get(f'https://api.kyber.network/quote_amount?base={token_1_address}&quote={token_2_address}&base_amount={5}&type=sell').json()
        #if buy_side['error'] == True or sell_side['error'] == True:
         #   raise
        print(f'{token}->{token2}: Buy {buy_side}, Sell {sell_side}')
        bid_float = sell_side['data']
        ask_float = buy_side['data']
        redis_client.set(f'kyber,{token},{token2}',f'{bid_float},{ask_float}')
    except Exception as e:
        print(e)
"""



#Do task every 5 seconds




#Triangle_Calculations
#starting pairs must be ETH, DAI, USDC

