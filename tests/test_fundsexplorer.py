import pytest

from margemliquida_market_data.fundsexplorer import fundsexplorer


def test_buscar_df_fiis():
    df = fundsexplorer.buscar_dados_fundsexplorer()
    assert len(df) > 0
    assert len(df.columns) == 8

    colunas = [
        "Código",
        "Setor",
        "Liquidez Diária (R$)",
        "P/VP",
        "Dividend Yield",
        "Variação Preço",
        "Patrimônio Líquido",
        "Num. Cotistas",
    ]

    assert colunas == list(df.columns)
