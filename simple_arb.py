import requests
import os
import sys

from decimal import Decimal

tokenlist = {
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

token1 = 'LINK'
token2 = 'USDC'
token_list = [t for t in requests.get('https://flash4all.net/api/tokens').json() if t != "REP"]
# token1 = input('What is your base collateral ').upper().strip()
print(f'Flashing {token1}')

([x for x in token_list])
MARKETS_kyber = "kyber"
MARKETS_uniswap = "uniswap"
dex_uniswap = 'uniswap'
dex_kyber = 'kyber'
initial_amount_uniswap: int = 1000
initial_amount_kyber: int = 1000

def uniswap_to_kyber(token1, token2):
    uniswap_starting = requests.get(
        f'https://api-v2.dex.ag/price?from={token1}&to={token2}&fromAmount={initial_amount_uniswap}&dex={dex_uniswap}&limitAmount=').json()
    uniswap_token_2_total = Decimal(uniswap_starting.get('price')) * initial_amount_uniswap
    print(uniswap_token_2_total)
    kyber_end = requests.get(
        f'https://api-v2.dex.ag/price?from={token2}&to={token1}&fromAmount={uniswap_token_2_total}&dex={dex_kyber}&limitAmount=').json()
    token_1_end_total = Decimal(kyber_end.get('price')) * uniswap_token_2_total
    print (token_1_end_total)
    profit = initial_amount_uniswap - token_1_end_total
    if token_1_end_total > initial_amount_uniswap:
        return f' {profit}'
    else:
        return f'not profitable Uniswap<>Kyber'

def kyber_to_uniswap(token1, token2):
    kyber_starting = requests.get(
        f'https://api-v2.dex.ag/price?from={token1}&to={token2}&fromAmount={initial_amount_kyber}&dex={dex_kyber}').json()
    kyber_token_2_total = Decimal(kyber_starting.get('price')) * initial_amount_kyber
    print(kyber_token_2_total)
    uniswap_end = requests.get(
        f'https://api-v2.dex.ag/price?from={token2}&to={token1}&fromAmount={kyber_token_2_total}&dex={dex_uniswap}').json()
    token_1_end_total = Decimal(uniswap_end.get('price')) * kyber_token_2_total
    print(token_1_end_total)
    profit = initial_amount_kyber - token_1_end_total
    if token_1_end_total > initial_amount_kyber:
        return f' {profit}'
    else:
        return f'not profitable Kyber<>Uniswap'




print(uniswap_to_kyber(token1, token2))
print('___________')
print(kyber_to_uniswap(token1, token2))