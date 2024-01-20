import random

from margemliquida_market_data.meu_fundamentus import meu_fundamentus


def test_buscar_df_setores():
    df = meu_fundamentus.get_df_setores()
    assert len(df) > 0


def test_buscar_acoes_do_setor():
    df_setores = meu_fundamentus.get_df_setores()
    id_setor = random.choice(df_setores.index)
    df = meu_fundamentus.get_df_acoes_do_setor(id_setor)
    assert len(df) > 0


def test_get_df_fiis():
    df = meu_fundamentus.get_df_fiis()
    assert len(df) > 0


def test_get_df_acoes():
    df = meu_fundamentus.get_df_acoes()
    assert len(df) > 0
