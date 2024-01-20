from margemliquida_market_data.tesouro_transparente.tesouro_transparente import (
    TesouroTransparente,
)


def test_buscar_titulos_tesouro_direto():
    tt = TesouroTransparente()
    df = tt.buscar_titulos_tesouro_direto()
    assert len(df) > 0


def test_buscar_vendas_tesouro():
    tt = TesouroTransparente()
    df = tt.buscar_vendas_tesouro()
    assert len(df) > 0


def test_buscar_recompras_tesouro():
    tt = TesouroTransparente()
    df = tt.buscar_recompras_tesouro()
    assert len(df) > 0

    assert len(df) > 0
