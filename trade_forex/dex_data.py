import requests
import sys
import os
from decimal import Decimal
import json
from redis_client import redis_client

#market_prices = requests.get(f'https://api.kyber.network/market')
addresses = {
           'MKR': '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
           'DAI': '0x6b175474e89094c44da98b954eedeac495271d0f',
           'BAT': '0x0d8775f648430679a709e98d2b0cb6250d2887ef',
           'TUSD': '0x8dd5fbce2f6a956c3022ba3663759011dd51e73e',
           'USDT': '0xdac17f958d2ee523a2206206994597c13d831ec7',
           'SAI': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
           'ETH': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
           'USDC': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
           'OMG': '0xd26114cd6EE289AccF82350c8d8487fedB8A0C07',
           'WBTC': '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',
           'LINK': '0x514910771af9ca656af840dff83e8264ecf986ca',
           'ZRX': '0xe41d2489571d322189246dafa5ebde1f4699f498',
           'KNC': '0xdd974d5c2e2928dea5f71b9825b8b646686bd200'
}

token_list = [t for t in requests.get('https://flash4all.net/api/tokens').json() if t != "REP"]

input_flash_collateral = 'MKR'
#input_flash_collateral = input('Enter Flash Collateral').upper()
trade_path = 'USDT'
trade_path_2 = 'ETH'
#trade_path = input('Enter potential path')
([x for x in token_list])

#buying = ask price
#selling = bid price
def find_uniswap_bid_ask(token, token2):
   if token == 'SAI' or token2 == 'SAI' or token == 'USDT' or token2 == 'USDT' or token == 'OMG' or token2 == 'OMG':
       return

   dex_ = 'uniswap'
   initial_amount = Decimal(100)

   try:
   #bid price = sell price
   # buy side = ask price should be lower
       uniswap_sell_side = requests.get(
       f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount={initial_amount}&dex={dex_}').json()
       uniswap_token2_amount = Decimal(uniswap_sell_side.get('price')) * initial_amount

       uniswap_buy_side = requests.get(
       f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount={uniswap_token2_amount}&dex={dex_}').json()

       uniswap_bid_float = uniswap_sell_side.get('price')
       uniswap_ask_float = (1 / Decimal(uniswap_buy_side.get('price')))
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

   dex_2 = "kyber"
   initial_amount: int = 100
   try:
       kyber_sell_side = requests.get(
           f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount={initial_amount}&dex={dex_2}&limitAmount=').json()
       kyber_token2_amount = Decimal(kyber_sell_side.get('price')) * initial_amount
       kyber_buy_side = requests.get(
           f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount={kyber_token2_amount}&dex={dex_2}&limitAmount=').json()



       kyber_bid_float = kyber_sell_side.get('price')
       kyber_ask_float = (1 / Decimal(kyber_buy_side.get('price')))
       print(f'{token}->{token2}: Buy {kyber_ask_float}, Sell {kyber_bid_float}')
       redis_client.set(f'kyber,{token},{token2}',f'{kyber_bid_float},{kyber_ask_float}')
   except Exception as e:
       print(token, token2)
       exc_type, exc_obj, exc_tb = sys.exc_info()
       fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
       print(exc_type, fname, exc_tb.tb_lineno)
       return {'error': str(e)}

for token in token_list:
   [find_kyber_bid_ask(token, token2) for token2 in token_list if token != token2]
   [find_uniswap_bid_ask(token, token2) for token2 in token_list if token != token2]









"""
new goal define what is in the CSV FILE/DATABASE
then grab it in the triangle trade algo
logic for getting prices of everything
1.) get price for all the pairs (ask and bid)
2.) create a triangle with aave collateral types
Initial Collateral types here:
(WBTC, SNX, ZRX, REP, MANA, LINK, KNC,
BAT, LEND, ETH, BUSD, sUSD, USDT, TUSD, USDC, DAI)


Next steps of what I can do with out deon
Grab only the price of each pair ask and bid
Store this data somewhere and be able to call it for the actual triangle in a different file

"""




#Do task every 5 seconds




#Triangle_Calculations
#starting pairs must be ETH, DAI, USDC


