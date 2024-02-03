from margemliquida_market_data.b3.listas import Lista


def buscar_lista_bdrs_nao_patrocinados(
    mostrar_debug=False, forcar_webscrapping=False, headless=True, yfinance_format=True
):
    lista_bdr = Lista(
        forcar_webscrapping=forcar_webscrapping, selenium_headless=headless
    )
    lista_bdr.configurar_tipo_lista("BDRs não patrocinados")
    lista_bdr.configurar_url(
        "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/bdr?language=pt-br"
    )
    lista_bdr.configurar_nome_arquivo_csv("bdrs-nao-patrocinados.csv")
    # lista_bdr.configurar_tamanho_maximo_pagina("120")
    lista_bdr.executar(mostrar_debug)
    sufixo = "11.SA" if yfinance_format else "11"
    return [codigo.upper() + sufixo for codigo in lista_bdr.resultado["Código"]]


# import datetime
# import os
# import tempfile
# from io import StringIO
# from time import sleep

# import pandas as pd
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# from margemliquida_market_data.selenium_config.meu_firefox import (
#     configura_webdriver_firefox_normal,
# )


# def ajustar_tabela(wd):
#     print("> Ajustando tabela para fazer webscrapping")
#     url = [
#         "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/bdr?language=pt-br",
#     ]
#     wd.get("".join(url))

#     botao_todos = wd.find_element(
#         By.CSS_SELECTOR, "div.form-group>button.btn.btn-light"
#     )
#     botao_todos.click()
#     sleep(3)

#     resultados_por_pagina = Select(wd.find_element(By.ID, "selectPage"))
#     resultados_por_pagina.select_by_value("120")
#     sleep(3)

#     tipo = wd.find_element(By.ID, "nav-table-tab")
#     tipo.click()
#     sleep(3)


# def gravar_dados_em_arquivo(resultado, NOME_ARQUIVO):
#     print("===========================")
#     print(f"Gravando resultado em {NOME_ARQUIVO} da pasta temporária")
#     pasta_temp = tempfile.gettempdir()
#     resultado.to_csv(os.path.join(pasta_temp, NOME_ARQUIVO))


# def mostrar_dados(resultado: pd.DataFrame):
#     print("===========================")
#     print("Total listado: 824")
#     print("Tamanho: ", len(resultado))
#     print(resultado.head())
#     print(resultado.tail())


# def executar_web_scrapping(NOME_ARQUIVO):
#     resultado = None
#     with configura_webdriver_firefox_normal() as wd:
#         ajustar_tabela(wd)

#         while True:
#             tabela = wd.find_element(By.CSS_SELECTOR, "table")
#             html = tabela.get_attribute("innerHTML")

#             df = pd.read_html(StringIO("<table>" + html + "</table>"))[0]

#             # print("> Capturou a tabela")

#             if resultado is None:
#                 # print("> Dataframe final ainda é nulo...")
#                 resultado = df
#                 # print("> Dataframe final era nulo...")
#                 # print(resultado)
#             else:
#                 # print("> Dataframe final NÃO é nulo...")
#                 resultado = pd.concat([resultado, df], ignore_index=True)
#                 # print(resultado)

#             icone_proxima_pagina = wd.find_element(
#                 By.CSS_SELECTOR, "ul.ngx-pagination>li.pagination-next"
#             )
#             icone_proxima_pagina_habilitado = (
#                 "disabled" not in icone_proxima_pagina.get_attribute("class")
#             )

#             if icone_proxima_pagina_habilitado:
#                 icone_proxima_pagina.click()
#                 sleep(3)
#             else:
#                 break

#         mostrar_dados(resultado)
#         gravar_dados_em_arquivo(resultado, NOME_ARQUIVO)


# def arquivo_tem_mais_de_7_dias(arquivo):
#     # Obtém a data de criação do arquivo
#     data_criacao_arquivo = datetime.datetime.fromtimestamp(os.path.getctime(arquivo))

#     # Obtém a data atual
#     data_atual = datetime.datetime.now()

#     # Calcula a diferença entre as datas
#     diferenca = data_atual - data_criacao_arquivo

#     # Verifica se a diferença é maior que 7 dias
#     if diferenca.days > 7:
#         # os.remove(arquivo)
#         print(
#             f"O arquivo '{arquivo}' foi removido, pois tinha mais de 7 dias desde a sua criação."
#         )
#     else:
#         print(
#             f"O arquivo '{arquivo}' tem menos de 7 dias desde a sua criação e não foi removido."
#         )


# # main

# NOME_ARQUIVO = "bdrs-nao-patrocinados.csv"
# PASTA_TEMP = tempfile.gettempdir()
# PATH_ARQUIVO = os.path.join(PASTA_TEMP, NOME_ARQUIVO)

# if os.path.exists(PATH_ARQUIVO):
#     if arquivo_tem_mais_de_7_dias(PATH_ARQUIVO):
#         os.remove(PATH_ARQUIVO)
#         executar_web_scrapping(PATH_ARQUIVO)
#     else:
#         mostrar_dados(pd.read_csv(PATH_ARQUIVO))
# else:
#     executar_web_scrapping(PATH_ARQUIVO)
