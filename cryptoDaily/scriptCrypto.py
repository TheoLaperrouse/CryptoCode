import os
from binance.client import Client
import gspread
import time

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)

def get_price(coin_symbol, coins_info, devise):
    price = next(({'coin' : devise, 'value': float(coin['price'])}  for coin in coins_info if coin['symbol'] == coin_symbol+devise), None)
    print(coin_symbol+devise)
    print(price)
    return price

def get_avg_price_buy_sell(coin_symbol, devise):
    if coin_symbol != "USDT":
        orders = [order for order in client.get_all_orders(symbol=coin_symbol+devise) if order['status'] == 'FILLED']
        if len(orders)> 0:
            avg_buy = get_avg(orders, 'BUY')
            avg_sell = get_avg(orders, 'SELL')
            return {'BUY': avg_buy, 'SELL': avg_sell}
    return {'BUY': 1, 'SELL': f'Aucune vente de {coin_symbol}'}

def get_avg(orders, text):
    qty_sum =sum([float(order['executedQty']) for order in orders if order['side'] == text])
    price_sum =sum([float(order['cummulativeQuoteQty']) for order in orders  if order['side'] == text])
    return price_sum/qty_sum if qty_sum != 0 else 1

def update_crypto(my_assets,coins_info):
    gc = gspread.service_account()
    sheet = gc.open("Cryptomonnaie").sheet1  
    list_crypto = sheet.col_values(1)
    for crypto in my_assets: 
        if crypto["symbol"] in list_crypto :
            row = sheet.find(crypto["symbol"]).row
        else :
            row = len(list_crypto)+1
            sheet.update_cell(row, 1, crypto["symbol"]  )
            list_crypto.append(crypto['symbol'])
        sheet.update_cell(row, 4, crypto['number'])
        coin = sheet.cell(row,3).value 
        coin = "USDT" if coin == "USD" else coin
        price = get_price(crypto["symbol"],coins_info,coin) if coin != None else None
        sheet.update_cell(row, 5, price['value']) if price != None else None
        sheet.update_cell(row, 9, get_avg_price_buy_sell(crypto["symbol"],'USDT')['BUY'])
        sheet.update_cell(row, 10, get_avg_price_buy_sell(crypto["symbol"],'USDT')['SELL'])

def main():
    assets = client.get_account()['balances']
    coins_info = client.get_all_tickers()
    my_assets = [{'symbol' : asset['asset'],'number' : float(asset['free'])+float(asset['locked'])} 
                    for asset in assets if float(asset['free'])+float(asset['locked']) > 0]
    update_crypto(my_assets,coins_info)

if __name__ == "__main__":
    while True : 
        main()
        time.sleep(600)