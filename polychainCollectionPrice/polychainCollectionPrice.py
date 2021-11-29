from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pycoingecko import CoinGeckoAPI
import time
import re

s=Service(ChromeDriverManager().install())
cg = CoinGeckoAPI()
regExp_attribute = "meta_text_0=([a-zA-Z]*)&meta_text_1=([a-z A-Z]*)&meta_text_2=([a-z A-Z]*)&meta_text_3=([a-z A-Z]*)"
price_bnb = cg.get_price(ids="binancecoin", vs_currencies='EUR')["binancecoin"]['eur']
xpath = "/html/body/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[1]/div[3]/div[2]/span[2]"
user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
links_polychain = []
prix_total = 0

with open(file='polychainMonsters.html',mode='r') as html:
    soup = BeautifulSoup(html, 'html.parser')
## To change with the class of the TofuNFT Button
attributes = soup.find_all('a',{"class":"boosterCardstyle__OpenSeaButton-sc-wkk6t8-27 hvVrpI"})

for attribute in attributes:
    links_polychain.append(attribute['href'])
print(f'{len(links_polychain)} PolychainMonsters')

for link in links_polychain:
    options = Options()
    options.headless = True
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=s,options=options)
    driver.get(link+'&category=fixed-price&isBundle=0')
    time.sleep(10)
    prixMin = float(driver.find_element(By.XPATH, xpath).text.split()[0]) if driver.find_element(By.XPATH, xpath).text.split()[0] else 0
    attributes = re.search(regExp_attribute,link)
    print(f'{attributes.group(1)} {attributes.group(2)} {attributes.group(3)} {attributes.group(4)} : {prixMin} BNB ({round(prixMin * price_bnb, 2)} €)')
    prix_total += prixMin
    driver.quit()
print(f'Votre collection a un prix estimé de {prix_total} BNB soit {round(prix_total * price_bnb, 2)} €')