from pycoingecko import CoinGeckoAPI
import time
import subprocess

cg = CoinGeckoAPI()

id = input("Renseigner l'id de la cryptomonnaie que vous souhaitez vendre : ")

vs_currencies = input("Renseigner la cryptomonnaie dans laquel vous souhaitez voir votre première crypto : ")

price_alert = float(input("Renseigner le prix au-dessus duquel vous souhaitez être alerter : "))

while True:
    #exemple : cg.get_price(ids='polychain-monsters', vs_currencies='bnb')
    price = float(cg.get_price(ids=id, vs_currencies=vs_currencies)[id][vs_currencies])
    print(price)
    if price > price_alert :
        subprocess.call(['notify-send','Alerte Crypto',f'Le {id} est à {price} {vs_currencies.capitalize()}'])
    time.sleep(60)