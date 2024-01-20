from margemliquida_market_data.meu_fundamentus import meu_fundamentus


def test_buscar_df_setores():
    df = meu_fundamentus.get_df_setores()
    assert len(df) > 0
