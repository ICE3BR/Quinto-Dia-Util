import pytest
from utils import calcular_quinto_dia_util, formatar_data_extenso

# Substitua por um token válido para rodar testes reais
TOKEN_FAKE = "123456789"

# Mock: sobrescrevemos a função de obter feriados para isolar os testes
import utils

def fake_obter_feriados(ano, estado, token):
    return set(["2025-01-01", "2025-01-20", "2025-01-25"])  # Feriados em janeiro 2025

utils.obter_feriados = fake_obter_feriados

def test_quinto_dia_util_sem_sabado():
    dias = calcular_quinto_dia_util(2025, 1, "SP", TOKEN_FAKE, contar_sabado=False)
    assert len(dias) >= 5
    assert isinstance(dias[4], str)

def test_quinto_dia_util_com_sabado():
    dias = calcular_quinto_dia_util(2025, 1, "SP", TOKEN_FAKE, contar_sabado=True)
    assert len(dias) >= 5
    assert isinstance(dias[4], str)

def test_menos_de_cinco_dias_uteis():
    dias = calcular_quinto_dia_util(2025, 2, "SP", TOKEN_FAKE, contar_sabado=False)
    dias_cortado = dias[:4]  # simula mês com 4 dias úteis
    assert len(dias_cortado) == 4

def test_formatar_data_extenso():
    data = "2025-03-12"
    data_formatada, dia_semana, mes_nome = formatar_data_extenso(data)
    assert data_formatada == "12/03/2025"
    assert dia_semana == "Quarta-feira"
    assert mes_nome == "Março"

if __name__ == "__main__":
    pytest.main([__file__])