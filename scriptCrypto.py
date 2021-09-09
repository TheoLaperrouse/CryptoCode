import os
from binance.client import Client

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')


def get_price(coin_symbol, coins_info):
    price = next(({'coin' : 'EUR', 'value': float(coin['price'])}  for coin in coins_info if coin['symbol'] == coin_symbol+'EUR'), 
                next(({'coin' : 'USDT', 'value': float(coin['price'])} for coin in coins_info if coin['symbol'] == coin_symbol+'USDT'), 
                    None))
    return price

def main():
    client = Client(api_key, api_secret)
    assets = client.get_account()['balances']
    coins_info = client.get_all_tickers()
    my_assets = [{'symbol' : asset['asset'],'number' : float(asset['free'])+float(asset['locked']), 'price': get_price(asset['asset'], coins_info) } 
                    for asset in assets if float(asset['free'])+float(asset['locked']) > 0]
    print(my_assets)
    total_price = sum([asset['number']*asset['price']['value'] for asset in my_assets if asset['price'] != None])
    print(total_price)

if __name__ == "__main__":
    main()