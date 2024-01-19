from margemliquida_market_data.fundsexplorer import fundsexplorer


def test_buscar_df_fiis():
    df = fundsexplorer.buscar_dados_fundsexplorer()
    assert len(df) > 0
