import requests
import calendar
from datetime import datetime
import locale
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
token = os.getenv("API_TOKEN")
if not token:
    raise EnvironmentError("Token da API não encontrado no .env.")

# Tenta configurar locale para exibir dia e mês em português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    pass

def obter_feriados(ano, estado, token):
    url = f"https://api.invertexto.com/v1/holidays/{ano}?token={token}&state={estado}"
    response = requests.get(url)
    if response.status_code == 200:
        feriados = response.json()
        return set(feriado['date'] for feriado in feriados)
    else:
        raise Exception(f"Erro ao obter feriados: {response.status_code} - {response.text}")

def calcular_quinto_dia_util(ano, mes, estado, token, contar_sabado=False):
    feriados = obter_feriados(ano, estado, token)
    dias_uteis = []
    _, num_dias = calendar.monthrange(ano, mes)

    for dia in range(1, num_dias + 1):
        data = datetime(ano, mes, dia)
        if data.weekday() < 5 or (contar_sabado and data.weekday() == 5):
            data_str = data.strftime('%Y-%m-%d')
            if data_str not in feriados:
                dias_uteis.append(data_str)

    return dias_uteis

def entrada_usuario():
    while True:
        estado = input("Informe o estado (UF, ex: SP): ").strip().upper()
        if len(estado) == 2 and estado.isalpha():
            break
        print("UF inválida. Digite exatamente 2 letras.")

    while True:
        try:
            mes = int(input("Informe o mês (1 a 12): "))
            if 1 <= mes <= 12:
                break
            else:
                print("Mês fora do intervalo válido.")
        except ValueError:
            print("Digite um número inteiro para o mês.")

    while True:
        try:
            ano = int(input("Informe o ano (ex: 2025): "))
            break
        except ValueError:
            print("Ano inválido. Digite um número inteiro.")

    while True:
        contar_sabado_input = input("Contar sábados? [Y/N]: ").strip().upper()
        if contar_sabado_input in ['Y', 'N']:
            contar_sabado = contar_sabado_input == 'Y'
            break
        print("Opção inválida. Digite Y ou N.")

    return estado, mes, ano, contar_sabado

if __name__ == "__main__":
    estado, mes, ano, contar_sabado = entrada_usuario()
    dias_uteis = calcular_quinto_dia_util(ano, mes, estado, token, contar_sabado)

    if len(dias_uteis) >= 5:
        data_obj = datetime.strptime(dias_uteis[4], '%Y-%m-%d')
        data_formatada = data_obj.strftime('%d/%m/%Y')
        dia_semana = data_obj.strftime('%A').capitalize()
        nome_mes = data_obj.strftime('%B').capitalize()
        print(f"O quinto dia útil de {nome_mes} ({mes:02d}/{ano}) em {estado} é {data_formatada} ({dia_semana}).")
    else:
        print(f"Atenção: o mês {mes:02d}/{ano} em {estado} possui apenas {len(dias_uteis)} dia(s) útil(is):")
        for dia in dias_uteis:
            data_obj = datetime.strptime(dia, '%Y-%m-%d')
            print(f" - {data_obj.strftime('%d/%m/%Y')} ({data_obj.strftime('%A').capitalize()})")
