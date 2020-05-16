import requests
from decimal import Decimal
import json
from redis_client import redis_client
dex_ = 'uniswap'
srcToken = 'DAI'
destToken = 'ETH'
initial_amount = input('How much we flashing')
uniswap_make_shift = requests.get(f'https://api-v2.dex.ag/price?from={srcToken}&to={destToken}&fromAmount={initial_amount}&dex={dex_}&limitAmount=').json()
print(uniswap_make_shift)

"""
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

uniswap_addresses = {
            'DAI': 'ETH_0x97deC872013f6B5fB443861090ad931542878126',
            'USDC': 'ETH_0xe9Cf7887b93150D4F2Da7dFc6D502B216438F244',
            'MKR': 'ETH_0x4d2f5cFbA55AE412221182D8475bC85799A5644b',
            'WBTC': 'ETH_0xA2881A90Bf33F03E7a3f803765Cd2ED5c8928dFb',
            'Link': 'ETH_0x2E642b8D59B45a1D8c5aEf716A84FF44ea665914',
            'BAT' : 'ETH_0x3958B4eC427F8fa24eB60F42821760e88d485f7F',
            'ETH' : 'ETH_0x05cDe89cCfa0adA8C88D5A23caaa79Ef129E7883',
            'TUSD': 'ETH_0x1aEC8F11A7E78dC22477e91Ed924Fab46e3A88Fd',
            'USDT' : 'Eth_0x000000x000x0x0x00x0x0x0x0x0x0x0x00x0xx0',
            'SAI' : 'Eth_0x000000x000x0x0x00x0x0x0x0x0x0x0x00x0xx0'
}

token_list = [t for t in requests.get('https://flash4all.net/api/tokens').json() if t != "REP"]

input_flash_collateral = 'MKR'
#input_flash_collateral = input('Enter Flash Collateral').upper()
trade_path = 'USDT'
trade_path_2 = 'ETH'
#trade_path = input('Enter potential path')

def find_uniswap_bid_ask(token_2):
    token_quote = uniswap_addresses[token_2]
    token_base_ETH = 'ETH'
    try:
        ask_bid_eth_only = requests.get(f'https://api.uniswap.info/v1/orderbook/{token_quote}').json()
        print(ask_bid_eth_only)
    except Exception as p:
        print(p)


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
    [find_uniswap_bid_ask(token2) for token2 in token_list]


"""






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

