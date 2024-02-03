from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def configura_webdriver_firefox():
    options = Options()
    driver = webdriver.Firefox(options=options)
    return driver


def configura_webdriver_chrome():
    options = Options()
    driver = webdriver.Chrome(options=options)
    return driver


# Para corrigir problemas que acontecem no firefox
def scroll_shim(passed_in_driver, object):
    x = object.location["x"]
    y = object.location["y"]
    scroll_by_coord = "window.scrollTo(%s,%s);" % (x, y)
    scroll_nav_out_of_way = "window.scrollBy(0, -120);"
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def fazer_scroll_final_pagina(wd):
    sleep(2)
    scroll_pause_time = 1
    screen_height = wd.execute_script("return window.screen.height;")
    i = 1

    while True:
        wd.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(
                screen_height=screen_height, i=i
            )
        )
        i += 1
        sleep(scroll_pause_time)
        scroll_height = wd.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            break


def buscar_e_imprimir_caracteristicas(item):
    try:
        lista_caracteristicas = item.find_elements(
            By.CSS_SELECTOR, "ul.olx-ad-card__labels-items>li>span"
        )

        # print(f"Link: {link}")
        for caract in lista_caracteristicas:
            descricao = caract.get_attribute("aria-label")
            print(f"Característica: {descricao}")
    except Exception:
        print("Característica: Erro ao buscar as características do imóvel.")


def buscar_e_imprimir_localizacao(item):
    try:
        localizacao = item.find_element(
            By.CSS_SELECTOR, "div.olx-ad-card__location-date-container>p"
        ).text
    except NoSuchElementException:
        localizacao = "Erro ao buscar a localização."
    print(f"Localização: {localizacao}")


def buscar_e_imprimir_preco(item):
    try:
        preco = item.find_element(By.CSS_SELECTOR, "h3.olx-ad-card__price").text
    except NoSuchElementException:
        preco = "Erro ao buscar o preço."
    print(f"Preço: {preco}")


def buscar_e_imprimir_titulo(item):
    try:
        titulo = item.find_element(By.CSS_SELECTOR, "a.olx-ad-card__title-link").text
    except NoSuchElementException:
        titulo = "Erro ao buscar o título"
    print(f"Titulo: {titulo}")


def posiciona_item_na_tela(wd, item):
    scroll_shim(wd, item)
    actions = ActionChains(wd)
    actions.move_to_element(item).perform()


def olx():
    URL = "https://www.olx.com.br/imoveis/venda/estado-sc/florianopolis-e-regiao/sul"
    with configura_webdriver_chrome() as wd:
        wd.get(URL)
        # fazer_scroll_final_pagina(wd)

        # Busca todos os cards
        lista = wd.find_elements(
            By.CSS_SELECTOR, "#main-content>div:nth-child(4)>div.renderIfVisible"
        )

        # print("Tamanho da lista " + str(len(lista)))
        for item in lista:
            posiciona_item_na_tela(wd, item)
            buscar_e_imprimir_titulo(item)
            buscar_e_imprimir_preco(item)
            buscar_e_imprimir_localizacao(item)
            buscar_e_imprimir_caracteristicas(item)
            print("==================")


olx()
