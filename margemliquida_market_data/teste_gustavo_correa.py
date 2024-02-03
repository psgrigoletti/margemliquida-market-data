from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def configura_webdriver_firefox():
    firefox_options = Options()
    # firefox_options.headless = True
    # firefox_options.add_argument("--headless")
    # firefox_options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=firefox_options)
    return driver


def scroll_shim(passed_in_driver, object):
    x = object.location["x"]
    y = object.location["y"]
    scroll_by_coord = "window.scrollTo(%s,%s);" % (x, y)
    scroll_nav_out_of_way = "window.scrollBy(0, -120);"
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def teste2():
    URL = "https://www.olx.com.br/imoveis/venda/estado-sc/florianopolis-e-regiao/sul"
    with configura_webdriver_firefox() as wd:
        wd.get(URL)
        sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = (
            1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        )
        screen_height = wd.execute_script(
            "return window.screen.height;"
        )  # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time
            wd.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(
                    screen_height=screen_height, i=i
                )
            )
            i += 1
            sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = wd.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        lista = wd.find_elements(
            By.CSS_SELECTOR, "#main-content>div:nth-child(4)>div.renderIfVisible"
        )

        print("Tamanho da lista " + str(len(lista)))
        for item in lista:
            scroll_shim(wd, item)
            actions = ActionChains(wd)
            actions.move_to_element(item).perform()
            # link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").value
            try:
                titulo = item.find_element(
                    By.CSS_SELECTOR, "a.olx-ad-card__title-link"
                ).text
            except NoSuchElementException:
                titulo = "Erro ao buscar o título"

            try:
                preco = item.find_element(By.CSS_SELECTOR, "h3.olx-ad-card__price").text
            except NoSuchElementException:
                preco = "Erro ao buscar o preço."

            try:
                localizacao = item.find_element(
                    By.CSS_SELECTOR, "div.olx-ad-card__location-date-container>p"
                ).text
            except NoSuchElementException:
                localizacao = "Erro ao buscar a localização."

            lista_caracteristicas = item.find_elements(
                By.CSS_SELECTOR, "ul.olx-ad-card__labels-items>li>span"
            )

            # print(f"Link: {link}")
            print(f"Titulo: {titulo}")
            print(f"Preço: {preco}")
            print(f"Localização: {localizacao}")
            for caract in lista_caracteristicas:
                descricao = caract.get_attribute("aria-label")
                print(f"Característica: {descricao}")

            print("==================")


teste2()


def teste1():
    MAXIMO_PAGINAS = 3
    contador_paginas = 1
    URL = "https://www.vivareal.com.br/venda/santa-catarina/palhoca/"
    TEMPO_AGUARDAR = 15

    with configura_webdriver_firefox() as wd:
        wd.get(URL)

        aceitar_cookies = wd.find_element(
            By.CSS_SELECTOR, "button.cookie-notifier__cta"
        )
        if aceitar_cookies:
            print("Vou clicar no botão para aceitar os cookies.")
            aceitar_cookies.click()
            print("Cliquei no botão para aceitar os cookies.")

        while True:
            lista = None
            itens = None

            print(f"Vou aguardar {TEMPO_AGUARDAR} segundos.")
            sleep(TEMPO_AGUARDAR)
            print(f"Aguardei {TEMPO_AGUARDAR} segundos.")

            lista = wd.find_element(By.CSS_SELECTOR, "div.results-list")
            print("Achei uma lista de imóveis.")

            itens = lista.find_elements(By.CSS_SELECTOR, "div.property-card__content")
            print(f"A lista de imóveis tem {len(itens)} itens.")

            for numero, item in enumerate(itens):
                if len(item.text) > 0:
                    print(f"Página {contador_paginas} - Imóvel {numero+1}")
                    print(item.text)
                    print("===========================")

            botao = wd.find_element(By.CSS_SELECTOR, "button[title='Próxima página']")

            if botao and contador_paginas < MAXIMO_PAGINAS:
                print("Vou clicar no botão 'Próxima página'.")
                botao.click()
                print("Cliquei no botão 'Próxima página'.")
                contador_paginas += 1
            else:
                break

        # wd.close()
        # wd.close()
        # wd.close()
