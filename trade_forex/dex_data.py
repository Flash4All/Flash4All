import requests
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
            'ETH': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
        }

token_list = [t for t in requests.get('https://flash4all.net/api/tokens').json() if t != "REP"]

input_flash_collateral = 'MKR'
#input_flash_collateral = input('Enter Flash Collateral').upper()
trade_path = 'USDT'
trade_path_2 = 'ETH'
#trade_path = input('Enter potential path')
collateral_total = '1'
flash_collateral_address = addresses[f'{input_flash_collateral}']
token_2 = addresses[f'{trade_path}']
token_3 = addresses[f'{trade_path_2}']

#things that happen only once
#token_list = requests.get(f'https://api.kyber.network/buy_rate?id={token_id}&qty=10').json()
wallet_id = '0x0859A7958E254234FdC1d200b941fFdfCAb02fC1'
user_address = '0x000000000'


sell_or_buy_1 = 'sell'
sell_or_buy_2 = 'sell'
sell_or_buy_3 = 'sell'
print()


def find_reversal():
    pass
"""
#1inch_token_list = no token list call
#([x['symbol'] for x in token_list])
"""

def find_uniswap_bid_ask(token, token2):
    pass

def find_kyber_bid_ask(token, token2):
    token_1_address = addresses[token]
    token_2_address = addresses[token2]
    try:
        buy_side = requests.get(f'https://api.kyber.network/quote_amount?base={token_1_address}&quote={token_2_address}&base_amount={1}&type=buy').json()
        sell_side = requests.get(f'https://api.kyber.network/quote_amount?base={token_1_address}&quote={token_2_address}&base_amount={1}&type=sell').json()
        if buy_side['error'] == True or sell_side['error'] == True:
            raise
        print(f'{token}->{token2}: Buy {buy_side}, Sell {sell_side}')
        bid_float = sell_side['data']
        ask_float = buy_side['data']
        redis_client.set(f'kyber,{token},{token2}',f'{bid_float},{ask_float}')
    except Exception as e:
        print(e)

for token in token_list:
    [find_kyber_bid_ask(token, token2) for token2 in token_list if token != token2]
    [find_uniswap_bid_ask(token, token2) for token2 in token_list if token != token2]


print(redis_client.get('DAI,ETH').decode())
print(redis_client.get('ETH,DAI').decode())






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

