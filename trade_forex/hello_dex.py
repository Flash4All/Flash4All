import requests

response1 = requests.get ('https://api-v2.dex.ag/token-list-full')
response = requests.get('https://api-v2.dex.ag/price?from=ETH&to=DAI&fromAmount=1&dex=ag')

print(response.status_code)
print(response.text)

print(response1.text)
#Triangle_Calculations
#starting pairs must be ETH, DAI, USDC

