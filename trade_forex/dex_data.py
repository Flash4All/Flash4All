import requests
from decimal import Decimal
import { ... } from '@uniswap/sdk'
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
            'REP': '0xe94327d07fc17907b4db788e5adf2ed424addff6'
        }


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
forward_trade_1 = requests.get(f'https://api.kyber.network/quote_amount?base={flash_collateral_address}&quote={token_2}&base_amount={collateral_total}&type={sell_or_buy_1}').json()
trade_2_quantity = forward_trade_1['data']
print(f'I now have {trade_2_quantity} {trade_path}')

forward_trade_2 =  requests.get(f'https://api.kyber.network/quote_amount?base={token_2}&quote={token_3}&base_amount={trade_2_quantity}&type={sell_or_buy_2}').json()
trade_3_quantity = forward_trade_2['data']
print(f'I now have {trade_3_quantity} {trade_path_2}')
forward_trade_3 = requests.get(f'https://api.kyber.network/quote_amount?base={token_3}&quote={flash_collateral_address}&base_amount={trade_3_quantity}&type={sell_or_buy_3}').json()
end_result = forward_trade_3['data']
print(f'I now have {end_result} of {input_flash_collateral}')

before = (Decimal(forward_trade_1['data']))
middle = (Decimal(forward_trade_2['data']))
after = (Decimal(forward_trade_3['data']))

quick_calc = after - 1
ratio_calculation = ((after/1)-1 )*100
print(ratio_calculation)
print(quick_calc)


def find_reversal()
"""
#1inch_token_list = no token list call
#([x['symbol'] for x in token_list])


def find_bid_ask(token, token2):
    try:
        bid_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount=1&dex=ag').json()
        ask_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount=1&dex=ag').json()
        ask_float = Decimal(ask_price1['price'])
        bid_float = 1/Decimal(bid_price1['price'])
        redis_client.set(f'{token},{token2}',f'{bid_float},{ask_float}')
    except Exception as e:
        print(e)
for token in token_list:
    [find_bid_ask(token, token2) for token2 in token_list if token != token2]


print(redis_client.get('DAI,ETH'))
#"""






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

