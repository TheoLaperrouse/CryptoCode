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

def get_average_price_buy(coin_symbol, devise):
    if coin_symbol != "USDT":
        orders = [order for order in client.get_all_orders(symbol=coin_symbol+devise) if order['status'] == 'FILLED' and order['side'] == 'BUY']
        if len(orders)> 0:
            qty_sum =sum([float(order['executedQty']) for order in orders])
            price_sum =sum([float(order['cummulativeQuoteQty']) for order in orders])
            avg = price_sum / qty_sum
            return avg    
    return 1


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
        if coin == "USD" :
            coin = "USDT"
        if coin != None:
            price = get_price(crypto["symbol"],coins_info,coin)
            if price != None:
                sheet.update_cell(row, 5, price['value'])
        sheet.update_cell(row, 9, get_average_price_buy(crypto["symbol"],'USDT'))



def main():
    assets = client.get_account()['balances']
    coins_info = client.get_all_tickers()
    my_assets = [{'symbol' : asset['asset'],'number' : float(asset['free'])+float(asset['locked'])} 
                    for asset in assets if float(asset['free'])+float(asset['locked']) > 0]
    update_crypto(my_assets,coins_info)
    

if __name__ == "__main__":
    while True : 
        main()
        time.sleep(300)