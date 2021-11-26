from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pycoingecko import CoinGeckoAPI
import time

s=Service(ChromeDriverManager().install())
cg = CoinGeckoAPI()
price_bnb = cg.get_price(ids="binancecoin", vs_currencies='EUR')["binancecoin"]['eur']
xpath = "/html/body/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[1]/div[3]/div[2]/span[2]"
links_polychain = []
prix_total = 0

with open(file='polychainMonster.html',mode='r') as html:
    soup = BeautifulSoup(html, 'html.parser')
attributes = soup.find_all('a',{"class":"boosterCardstyle__OpenSeaButton-sc-wkk6t8-27 hvVrpI"})

for attribute in attributes:
    if attribute['href'] not in links_polychain:
        links_polychain.append(attribute['href'])
print(f'{len(links_polychain)} PolychainMonsters')

for link in links_polychain:
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(link+'&category=fixed-price')
    time.sleep(10)
    prixMin = float(driver.find_element(By.XPATH, xpath).text.split()[0]) if driver.find_element(By.XPATH, xpath).text.split()[0] else 0
    print(prixMin)
    prix_total += prixMin
    driver.quit()

print(f'Votre collection a un prix estimé de {prix_total} BNB soit {prix_total * price_bnb}€')