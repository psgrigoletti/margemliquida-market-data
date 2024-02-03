import datetime
import os
import tempfile
from io import StringIO
from time import sleep

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from margemliquida_market_data.selenium_config.meu_firefox import (
    configura_webdriver_firefox,
    configura_webdriver_firefox_normal,
)


class Lista:
    """Classe que auxilia na realização de webscrapping das listas de ETFs e BDRs, no site da B3"""

    SEGUNDOS_ESPERA = 3
    PASTA_TEMP = tempfile.gettempdir()
    DIAS_MANTER_ARQUIVO_CSV = 7
    CSS_ICONE_PROXIMA_PAGINA = "ul.ngx-pagination>li.pagination-next"
    CSS_BOTAO_TODOS = "div>button.btn.btn-light"
    ID_BOTAO_TIPO_TABELA_LISTA = "nav-table-tab"

    def __init__(self, forcar_webscrapping: bool, selenium_headless: bool):
        self._nome_arquivo = None
        self._path_arquivo = None

        self.url = None
        self.tamanho_maximo_pagina = None
        self.forcar_webscrapping = forcar_webscrapping
        self.tipo_lista = None

        self.resultado = None
        self.selenium_headless = selenium_headless
        self.debug = False

        if self.selenium_headless:
            self._wd = configura_webdriver_firefox()
        else:
            self._wd = configura_webdriver_firefox_normal()

    def configurar_url(self, url):
        """Configura a URL onde será feito o webscrapping webscrapping."""
        self.url = url

    def configurar_tamanho_maximo_pagina(self, tamanho):
        """Configura o nome tamanho máximo de 'Resultados por página' para
        otimizar o webscrapping."""
        self.tamanho_maximo_pagina = tamanho

    def configurar_tipo_lista(self, tipo_lista):
        """Configura o nome da lista de resultados."""
        self.tipo_lista = tipo_lista

    def configurar_nome_arquivo_csv(self, nome_arquivo):
        """Configura o nome do arquivo CSV gravado com o resultado do
        webscrapping."""
        self._nome_arquivo = nome_arquivo

    def _arquivo_tem_mais_de_x_dias(self):
        # Obtém a data de criação do arquivo
        data_criacao_arquivo = datetime.datetime.fromtimestamp(
            os.path.getctime(self._path_arquivo)
        )

        # Obtém a data atual
        data_atual = datetime.datetime.now()

        # Calcula a diferença entre as datas
        diferenca = data_atual - data_criacao_arquivo

        # Verifica se a diferença é maior que DIAS_MANTER_ARQUIVO_CSV dias
        return diferenca.days > self.DIAS_MANTER_ARQUIVO_CSV

    def _mostrar_dados(self):
        print("===========================")
        print(self.tipo_lista)
        print("Tamanho:", len(self.resultado))
        print("")
        print("Primeiras 5 linhas")
        print(self.resultado.head(5))
        print("")
        print("Últimas 5 linhas")
        print(self.resultado.tail(5))

    def _gravar_dados_em_arquivo(self):
        self._imprimir_se_debug("===========================")
        self._imprimir_se_debug(
            f"Gravando resultado em {self._path_arquivo} (pasta temporária do sistema)"
        )
        self.resultado.to_csv(self._path_arquivo)

    def _executar_web_scrapping(self):
        self.resultado = None
        with self._wd:
            self._wd.get(self.url)
            self._ajustar_tabela()

            while True:
                self._capturar_dados_tabela()
                if not self._paginar():
                    break

            self._mostrar_dados()
            self._gravar_dados_em_arquivo()

    def _capturar_dados_tabela(self):
        tabela = self._wd.find_element(By.CSS_SELECTOR, "table")
        html = tabela.get_attribute("innerHTML")
        df = pd.read_html(StringIO("<table>" + html + "</table>"))[0]
        if self.resultado is None:
            self.resultado = df
        else:
            self.resultado = pd.concat([self.resultado, df], ignore_index=True)

    def _paginar(self):
        try:
            icone_proxima_pagina = self._wd.find_element(
                By.CSS_SELECTOR, self.CSS_ICONE_PROXIMA_PAGINA
            )
            icone_proxima_pagina_habilitado = (
                "disabled" not in icone_proxima_pagina.get_attribute("class")
            )

            if icone_proxima_pagina_habilitado:
                icone_proxima_pagina.click()
                sleep(self.SEGUNDOS_ESPERA)
                return True
            else:
                return False
        except NoSuchElementException as ex:
            print("Não encontrou o paginador...")
            return False

    def _imprimir_se_debug(self, texto):
        if self.debug:
            print(texto)

    def executar(self, debug):
        """Inicia o processo de webscrapping."""
        self.debug = debug
        self._path_arquivo = os.path.join(self.PASTA_TEMP, self._nome_arquivo)

        if os.path.exists(self._path_arquivo) and not self.forcar_webscrapping:
            if self._arquivo_tem_mais_de_x_dias():
                os.remove(self._path_arquivo)
                self._executar_web_scrapping()
            else:
                self._imprimir_se_debug(
                    f"Pegando dados do arquivo {self._path_arquivo}."
                )
                self.resultado = pd.read_csv(self._path_arquivo)
                self._mostrar_dados()
        else:
            self._executar_web_scrapping()

    def _ajustar_tabela(self):
        """Faz as configurações necessárias na tabela para executar o webscrapping."""
        botao_todos = self._wd.find_element(By.CSS_SELECTOR, self.CSS_BOTAO_TODOS)
        botao_todos.click()
        sleep(self.SEGUNDOS_ESPERA)

        try:
            resultados_por_pagina = Select(self._wd.find_element(By.ID, "selectPage"))

            if self.tamanho_maximo_pagina is None:
                self.tamanho_maximo_pagina = max(
                    [int(option.text) for option in resultados_por_pagina.options]
                )

            resultados_por_pagina.select_by_visible_text(
                str(self.tamanho_maximo_pagina)
            )
            sleep(self.SEGUNDOS_ESPERA)
        except NoSuchElementException as ex:
            print(f"Não encontrou paginador em {self.url}")
            print(ex)

        tipo = self._wd.find_element(By.ID, self.ID_BOTAO_TIPO_TABELA_LISTA)
        tipo.click()
        sleep(self.SEGUNDOS_ESPERA)


# main


# def buscar_bdrs(mostrar_debug=False, forcar_webscrapping=False, headless=True):
#     lista_bdr = Lista(
#         forcar_webscrapping=forcar_webscrapping, selenium_headless=headless
#     )
#     lista_bdr.configurar_tipo_lista("BDRs não patrocinados")
#     lista_bdr.configurar_url(
#         "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/bdr?language=pt-br"
#     )
#     lista_bdr.configurar_nome_arquivo_csv("bdrs-nao-patrocinados.csv")
#     # lista_bdr.configurar_tamanho_maximo_pagina("120")
#     lista_bdr.executar(mostrar_debug)
#     return [codigo.upper() + "34.SA" for codigo in lista_bdr.resultado["Código"]]


# def buscar_etfs_renda_variavel(
#     mostrar_debug=False, forcar_webscrapping=False, headless=True
# ):
#     lista_etf = Lista(
#         forcar_webscrapping=forcar_webscrapping, selenium_headless=headless
#     )
#     lista_etf.configurar_tipo_lista("ETFs renda variável")
#     lista_etf.configurar_url("https://sistemaswebb3-listados.b3.com.br/fundsPage/20")
#     lista_etf.configurar_nome_arquivo_csv("etfs-renda-variavel.csv")
#     # lista_etf.configurar_tamanho_maximo_pagina("60")
#     lista_etf.executar(mostrar_debug)
#     return [codigo.upper() + "11.SA" for codigo in lista_etf.resultado["Código"]]


# def buscar_etfs_renda_fixa(
#     mostrar_debug=False, forcar_webscrapping=False, headless=True
# ):
#     lista_etf = Lista(
#         forcar_webscrapping=forcar_webscrapping, selenium_headless=headless
#     )
#     lista_etf.configurar_tipo_lista("ETFs renda fixa")
#     lista_etf.configurar_url("https://sistemaswebb3-listados.b3.com.br/fundsPage/19")
#     lista_etf.configurar_nome_arquivo_csv("etfs-renda-fixa.csv")
#     # lista_etf.configurar_tamanho_maximo_pagina("60")
#     lista_etf.executar(mostrar_debug)
#     return [codigo.upper() + "11.SA" for codigo in lista_etf.resultado["Código"]]


# tickers_bdrs = buscar_bdrs(mostrar_debug=True)
# tickers_etfs_rv = buscar_etfs_renda_variavel(mostrar_debug=True)
# tickers_etfs_rf = buscar_etfs_renda_fixa(mostrar_debug=True)

# import random

# import matplotlib
# import yfinance as yf

# bdrs = yf.download(random.sample(tickers_bdrs, 10), start="2023-06-01")["Adj Close"]
# bdrs = bdrs.dropna(axis=1)
# bdrs = bdrs / bdrs.iloc[0]
# print(bdrs)
# bdrs.plot()

# etfs_rv = yf.download(random.sample(tickers_etfs_rv, 10), start="2023-06-01")[
#     "Adj Close"
# ]
# etfs_rv = etfs_rv.dropna(axis=1)
# etfs_rv = etfs_rv / etfs_rv.iloc[0]
# print(etfs_rv)
# etfs_rv.plot()

# etfs_rf = yf.download(random.sample(tickers_etfs_rf, 10), start="2023-06-01")["Close"]
# etfs_rf = etfs_rf.dropna(axis=1)
# etfs_rf = etfs_rf / etfs_rf.iloc[0]
# print(etfs_rf)
# etfs_rf.plot()
