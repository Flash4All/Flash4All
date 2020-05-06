import requests
from decimal import Decimal


#things that happen only once
dex_ag_token = requests.get('https://api-v2.dex.ag/token-list-full').json()
paraswap_token_list = requests.get('https://paraswap.io/api/v1/tokens/').json()
#1inch_token_list = no token list call
([x['symbol'] for x in dex_ag_token])


def find_bid_ask(token, token2):
    print(token, token2)
    bid_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount=1&dex=ag').json()
    ask_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount=1&dex=ag').json()
    ask_float = Decimal(ask_price1['price'].replace(',', '.'))
    bid_float = Decimal(bid_price1['price'].replace(',', '.'))
    print(f'BID PRICE {bid_float}, - ASK PRICE {ask_float}')

for token in dex_ag_token:
    [find_bid_ask(token['symbol'], token2['symbol']) for token2 in dex_ag_token if token['symbol'] != token2['symbol']]
    ask_1 = Decimal(ask_price1['price'].replace(',', '.'))

#change price from string to decimal/float






"""
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

