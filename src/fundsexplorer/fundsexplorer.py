""" Módulo que trabalha com os dados do site https://www.fundsexplorer.com.br/
"""

from io import StringIO
from time import sleep

import pandas as pd
from selenium_config import meu_firefox


def buscar_dados_fundsexplorer():
    """buscar_dados_fundsexplorer buscar dados dos FIIs no site https://www.fundsexplorer.com.br/ranking.

    Returns:
        df: DataFrame com os dados dos FIIs
    """
    url = "https://www.fundsexplorer.com.br/ranking"
    wd = meu_firefox.configura_webdriver_firefox()
    wd.get(url)
    sleep(8)
    html_content = wd.page_source
    df = pd.read_html(StringIO(str(html_content)), encoding="utf-8")[0]
    df.rename(columns={"Fundos": "Código"}, inplace=True)
    return df
