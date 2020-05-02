import requests
from decimal import Decimal



token_list = requests.get('https://api-v2.dex.ag/token-list-full').json()
token = input('What is your base collateral ').upper().strip()
print (f'Flashing {token}')
token2 = input('Pair 2 ').upper().strip()
token3 = input('Pair 3 ').upper().strip()
toke4 = 'USDC'
([x['symbol'] for x in token_list])

#pair 1 of the triangle eth/dai
bid_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token}&fromAmount=1&dex=ag').json()
ask_price1 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token2}&fromAmount=1&dex=ag').json()

#pair 2 of the triangle SAI/DAI
bid_price2 = requests.get(f'https://api-v2.dex.ag/price?from={token3}&to={token2}&fromAmount=1&dex=ag').json()
ask_price2 = requests.get(f'https://api-v2.dex.ag/price?from={token2}&to={token3}&fromAmount=1&dex=ag').json()

#pair 3 of the triangle ETH/SAI
bid_price3 = requests.get(f'https://api-v2.dex.ag/price?from={token3}&to={token}&fromAmount=1&dex=ag').json()
ask_price3 = requests.get(f'https://api-v2.dex.ag/price?from={token}&to={token3}&fromAmount=1&dex=ag').json()

#forward Triangle = Bid_Pair 1 * (1/ASK_Pair2) * (1/ASK_Pair3)



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
print(f'Expected Forward Return {forward_calculation_percent}')

#reversal calculation = Bid3* BID2 *(1/ASK1)
reversal_calculation = (bid_pair_3 * bid_pair_2 *(1/ask_pair_1) - 1)
reversal_calculation_percent = reversal_calculation * 100
print(f'Expected Reversal Return {reversal_calculation_percent}')
#if bid >= ask:
 #   print('possible error')








#forward Triangle = Bid_Pair 1 * (1/ASK_Pair2) * (1/ASK_Pair3)


#ask should almost always be higher than bid
#bid should be lower than ask



