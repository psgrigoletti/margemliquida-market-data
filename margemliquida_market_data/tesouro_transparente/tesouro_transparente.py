import logging
import time
from datetime import datetime, timedelta

import pandas as pd


class TesouroTransparente:
    """Classe que implementa acesso aos dados do Tesouro Transparente"""

    TESOURO_IPCA = "Tesouro IPCA+"
    TESOURO_IPCA_JUROS_SEMESTRAIS = "Tesouro IPCA+ com Juros Semestrais"
    TESOURO_SELIC = "Tesouro Selic"
    TESOURO_PREFIXADO = "Tesouro Prefixado"
    TESOURO_PREFIXADO_JUROS_SEMESTRAIS = "Tesouro Prefixado com Juros Semestrais"
    TAXA_COMPRA_MANHA = "Taxa Compra Manha"
    PU_BASE_MANHA = "PU Base Manha"
    VENCIMENTO_DO_TITULO = "Vencimento do Titulo"
    DATA_BASE = "Data Base"
    DATA_VENCIMENTO = "Data Vencimento"
    DATA_VENDA = "Data Venda"
    DATA_RESGATE = "Data Resgate"

    def __init__(self):
        self.titulos = None
        self.tipos_titulos = None
        self.hoje = None
        self.selic2025 = None
        self.selic2026 = None
        self.selic2027 = None
        self.selic2029 = None
        self.pre2025 = None
        self.pre2026 = None
        self.pre2029 = None
        self.pre2033 = None
        self.ipca2026 = None
        self.ipca2032 = None
        self.ipca2035 = None
        self.ipca2040 = None
        self.ipca2045 = None
        self.ipca2055 = None

    def atualizar_dados(self):
        logging.log(
            logging.INFO,
            "Buscando dados do site https://www.tesourotransparente.gov.br",
        )
        self.titulos = self.buscar_titulos_tesouro_direto()
        self.titulos.sort_index(inplace=True)
        self.tipos_titulos = (
            self.titulos.index.droplevel(level=1)
            .droplevel(level=1)
            .drop_duplicates()
            .to_list()
        )

        self._atualizar_dados_ipca()
        self._atualizar_dados_pre()
        self._atualizar_dados_selic()

    def buscar_titulos_tesouro_direto(self):
        url = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"
        df = pd.read_csv(url, sep=";", decimal=",")
        df[self.DATA_VENCIMENTO] = pd.to_datetime(
            df[self.DATA_VENCIMENTO], dayfirst=True
        )
        df[self.DATA_BASE] = pd.to_datetime(df[self.DATA_BASE], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[:, 3:]
        return df

    def buscar_vendas_tesouro(self):
        url = "https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv"
        df = pd.read_csv(url, sep=";", decimal=",")
        df[self.VENCIMENTO_DO_TITULO] = pd.to_datetime(
            df[self.VENCIMENTO_DO_TITULO], dayfirst=True
        )
        df[self.DATA_VENDA] = pd.to_datetime(df[self.DATA_VENDA], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[:, 3:]
        return df

    def buscar_recompras_tesouro(self):
        url = "https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/30c2b3f5-6edd-499a-8514-062bfda0f61a/download/RecomprasTesouroDireto.csv"
        df = pd.read_csv(url, sep=";", decimal=",")
        df[self.VENCIMENTO_DO_TITULO] = pd.to_datetime(
            df[self.VENCIMENTO_DO_TITULO], dayfirst=True
        )
        df[self.DATA_RESGATE] = pd.to_datetime(df[self.DATA_RESGATE], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[:, 3:]
        return df

    def _atualizar_dados_ipca(self):
        self.ipca2026 = self.titulos.loc[(self.TESOURO_IPCA, "2026-08-15")]
        self.ipca2032 = self.titulos.loc[
            (self.TESOURO_IPCA_JUROS_SEMESTRAIS, "2032-08-15")
        ]
        self.ipca2035 = self.titulos.loc[(self.TESOURO_IPCA, "2035-05-15")]
        self.ipca2040 = self.titulos.loc[
            (self.TESOURO_IPCA_JUROS_SEMESTRAIS, "2040-08-15")
        ]
        self.ipca2045 = self.titulos.loc[(self.TESOURO_IPCA, "2045-05-15")]
        self.ipca2055 = self.titulos.loc[
            (self.TESOURO_IPCA_JUROS_SEMESTRAIS, "2055-05-15")
        ]

    def _atualizar_dados_selic(self):
        self.selic2025 = self.titulos.loc[(self.TESOURO_SELIC, "2025-03-01")]
        self.selic2027 = self.titulos.loc[(self.TESOURO_SELIC, "2027-03-01")]

    def _atualizar_dados_pre(self):
        self.pre2025 = self.titulos.loc[(self.TESOURO_PREFIXADO, "2025-01-01")]
        self.pre2029 = self.titulos.loc[(self.TESOURO_PREFIXADO, "2029-01-01")]
        self.pre2033 = self.titulos.loc[
            (self.TESOURO_PREFIXADO_JUROS_SEMESTRAIS, "2033-01-01")
        ]
