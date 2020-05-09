import requests
from decimal import Decimal
from redis_client import redis_client

token1 = 'ETH'
token_list = requests.get('https://flash4all.net/api/tokens').json()
token1 = input('What is your base collateral ').upper().strip()
print(f'Flashing {token1}')

([x for x in token_list])


#forward Triangle = Bid_Pair 1 * (1/ASK_Pair2) * (1/ASK_Pair3)

def calculate_forward(token1, token2, token3):
    print('')
    trade_1 = redis_client.get(f'{token1},{token2}').decode().split(',')
    print(f'{token1},{token2},{trade_1}')
    trade_2 = redis_client.get(f'{token3},{token2}').decode().split(',')
    trade_3 = redis_client.get(f'{token1},{token3}').decode().split(',')
    forward_calculation = ((Decimal(trade_1[0])) * (1/Decimal(trade_2[1])) * (1/Decimal(trade_3[1])))-1
    print(f'{token2},{token3},{trade_2}')
    print(f'{token1},{token3},{trade_3}')
    forward_calculation_percent = forward_calculation * 100
    return (f'{token1},{token2},{token3}',forward_calculation_percent)

def get_tuple_calcutions(item):
    return item[1]

arbitriage_opps = []

for token2 in token_list:
    if token2 != token1:
        for token3 in token_list:
            if token3 != token1 and token3 != token2:
                arbitriage_opps.append(calculate_forward(token1, token2, token3))

arbitriage_opps.sort(reverse=True, key = get_tuple_calcutions)
print(arbitriage_opps[:3])

"""
#reversal calculation = Bid3* BID2 *(1/ASK1)
reversal_calculation = (bid_pair_3 * bid_pair_2 *(1/ask_pair_1) - 1)
reversal_calculation_percent = reversal_calculation * 100
print(f'Expected Reversal Return {reversal_calculation_percent}')
#if bid >= ask:
 #   print('possible error')
"""

"""
NOT USED ANYMORE
#pair 1 of the triangle eth/dai
bid_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount=1&dex=ag').json()
ask_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount=1&dex=ag').json()

#pair 2 of the triangle SAI/DAI
bid_price2 = requests.get(f'https://api-v2.dex.ag/price?from={token3}&to={token2}&fromAmount=1&dex=ag').json()
ask_price2 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token3}&fromAmount=1&dex=ag').json()

#pair 3 of the triangle ETH/SAI
bid_price3 = requests.get(f'https://api-v2.dex.ag/price?from={token3}&to={token}&fromAmount=1&dex=ag').json()
ask_price3 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token3}&fromAmount=1&dex=ag').json()



"""



