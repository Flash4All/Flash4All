import requests

def get_current_gas_prices():
    egs_response = requests.get('https://ethgasstation.info/api/ethgasAPI.json').json()
    fastest = egs_response['fastest']
    fast = egs_response['fast']
    average = egs_response['average']
    return {'fastest': fastest, 'fast': fast, 'average': average}

print(get_current_gas_prices())
