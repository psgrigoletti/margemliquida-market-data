from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from margemliquida_market_data.selenium_config.meu_firefox import (
    configura_webdriver_firefox_normal,
)

tickers_bdr = []

with configura_webdriver_firefox_normal() as wd:
    paginas = list(range(1, 3))
    for pagina in paginas:
        url = "https://maisretorno.com/lista-bdr"
        if pagina > 1:
            url = f"https://maisretorno.com/lista-bdr/page/{pagina}"

        print(f"Buscando página {url}")
        wd.get(url)

        for item in wd.find_elements(By.CSS_SELECTOR, "main>ul>li"):
            try:
                ticker = item.find_element(By.TAG_NAME, "a").text
                if len(ticker) == 6 and ticker.endswith("34"):
                    tickers_bdr.append(ticker)
                    print(f"Adicionando BDR {ticker}")
            except Exception as e:
                print("Não encontrou...")
                print(e)

quantidade = len(tickers_bdr)
print(f"Encontrou {quantidade} de BDRs")
print("São eles:")
print(tickers_bdr)

import matplotlib
import yfinance as yf

dados = yf.download([t + ".SA" for t in tickers_bdr[0:10]], start="2023-01-01")
fechamento = dados["Adj Close"]
fechamento.plot()

import redis

r = redis.Redis(
    host="redis-18360.c53.west-us.azure.cloud.redislabs.com",
    port=18360,
    password="LYNMWXMrqS9o4griad4afTOAvXBbiD0D",
)

r.set("bdrs", tickers_bdr)
print(r.get("bdrs"))
