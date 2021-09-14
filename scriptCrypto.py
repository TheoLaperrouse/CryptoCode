import os
from binance.client import Client
import gspread

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')



def get_price(coin_symbol, coins_info):
    price = next(({'coin' : 'EUR', 'value': float(coin['price'])}  for coin in coins_info if coin['symbol'] == coin_symbol+'EUR'), 
                next(({'coin' : 'USDT', 'value': float(coin['price'])} for coin in coins_info if coin['symbol'] == coin_symbol+'USDT'), 
                    None))
    return price

def update_crypto(symbol, price):
    return

def main():
    client = Client(api_key, api_secret)
    assets = client.get_account()['balances']
    coins_info = client.get_all_tickers()
    my_assets = [{'symbol' : asset['asset'],'number' : float(asset['free'])+float(asset['locked']), 'price': get_price(asset['asset'], coins_info) } 
                    for asset in assets if float(asset['free'])+float(asset['locked']) > 0]
    print(my_assets)
    total_price_eur = sum([asset['number']*asset['price']['value'] for asset in my_assets if asset['price'] != None and asset['price']['coin'] == 'EUR' ])
    total_price_usdt = sum([asset['number']*asset['price']['value'] for asset in my_assets if asset['price'] != None and asset['price']['coin'] == 'USDT']) * 0.85
    total_price = total_price_eur + total_price_usdt
    print(total_price)
    
    gc = gspread.service_account()
    wks = gc.open("Cryptomonnaie").sheet1

if __name__ == "__main__":
    main()