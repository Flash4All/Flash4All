import requests
from decimal import Decimal
import json
from redis_client import redis_client

#things that happen only once
token_list = requests.get('https://flash4all.net/api/tokens').json()
print(token_list)

#1inch_token_list = no token list call
#([x['symbol'] for x in token_list])

with open('trade_ask.csv', 'w') as json_file:
    pass
with open('trade_bid.csv', 'w') as json_file:
    pass

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

