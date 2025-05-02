import calendar
import locale
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
token = os.getenv("API_TOKEN")

# Tenta configurar para português (para nomes de dias e meses)
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    pass


def obter_feriados(ano, estado, token):
    url = f"https://api.invertexto.com/v1/holidays/{ano}?token={token}&state={estado}"
    response = requests.get(url)
    if response.status_code == 200:
        feriados = response.json()
        return set(feriado["date"] for feriado in feriados)
    else:
        raise Exception(
            f"Erro ao obter feriados: {response.status_code} - {response.text}"
        )


def calcular_quinto_dia_util(ano, mes, estado, token, contar_sabado=False):
    feriados = obter_feriados(ano, estado, token)
    dias_uteis = []
    _, num_dias = calendar.monthrange(ano, mes)

    for dia in range(1, num_dias + 1):
        data = datetime(ano, mes, dia)
        if data.weekday() < 5 or (contar_sabado and data.weekday() == 5):
            data_str = data.strftime("%Y-%m-%d")
            if data_str not in feriados:
                dias_uteis.append(data_str)

    if len(dias_uteis) >= 5:
        return dias_uteis[4]
    else:
        return None


# Entrada do usuário
estado = input("Informe o estado (UF, ex: SP): ").strip().upper()
mes = int(input("Informe o mês (1 a 12): "))
ano = int(input("Informe o ano (ex: 2025): "))
contar_sabado_input = input("Contar sábados? [Y/N]: ").strip().upper()
contar_sabado = contar_sabado_input == "Y"

quinto_dia_util = calcular_quinto_dia_util(ano, mes, estado, token, contar_sabado)
if quinto_dia_util:
    data_obj = datetime.strptime(quinto_dia_util, "%Y-%m-%d")
    data_formatada = data_obj.strftime("%d/%m/%Y")
    dia_semana = data_obj.strftime("%A").capitalize()
    nome_mes = data_obj.strftime("%B").capitalize()
    print(
        f"O quinto dia útil de {nome_mes} ({mes:02d}/{ano}) em {estado} é {data_formatada} ({dia_semana})."
    )
else:
    print(
        f"Não foi possível determinar o quinto dia útil para {mes:02d}/{ano} em {estado}."
    )
