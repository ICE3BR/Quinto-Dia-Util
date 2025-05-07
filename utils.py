import calendar
import locale
from datetime import datetime

import requests

# Tenta configurar locale para exibir dia e mês em português
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    pass

def formatar_data_feriado(data_iso):
    """
    Converte data no formato ISO (YYYY-MM-DD) para o formato DD/MM/YYYY
    """
    partes = data_iso.split('-')
    if len(partes) == 3:
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
    return data_iso  # Retorna o original se não conseguir formatar

def listar_feriados(ano, estado, token, mes=None):
    """
    Função para obter os feriados nacionais e estaduais.
    - ano: Ano a ser consultado.
    - estado: Código da UF (ex: 'SP', 'RJ').
    - mes: Mês (opcional, se informado retorna os feriados do mês específico).
    """
    url = f"https://api.invertexto.com/v1/holidays/{ano}"
    headers = {'Authorization': f'Bearer {token}'}
    params = {'state': estado} if estado else {}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception("Erro ao obter feriados")

    feriados = response.json()
    if mes:
        # Filtra os feriados do mês se 'mes' for passado
        feriados = [f for f in feriados if int(f['date'].split('-')[1]) == mes]
    
    return feriados


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

    return dias_uteis


def formatar_data_extenso(data_str):
    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    dias_semana = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]
    data_obj = datetime.strptime(data_str, "%Y-%m-%d")
    data_formatada = data_obj.strftime("%d/%m/%Y")
    dia_semana = dias_semana[data_obj.weekday()]
    nome_mes = meses[data_obj.month - 1]
    return data_formatada, dia_semana, nome_mes


def calcular_quintos_dias_util_ano_completo(ano, estado, token, contar_sabado=False):
    resultados = []
    for mes in range(1, 13):
        dias_uteis = calcular_quinto_dia_util(ano, mes, estado, token, contar_sabado)
        if len(dias_uteis) >= 5:
            data_formatada, dia_semana, nome_mes = formatar_data_extenso(dias_uteis[4])
            resultados.append(
                {
                    "mes": nome_mes,
                    "data": data_formatada,
                    "dia_semana": dia_semana,
                    "numero_mes": mes,
                }
            )
        else:
            resultados.append(
                {
                    "mes": datetime(ano, mes, 1).strftime("%B").capitalize(),
                    "data": None,
                    "dia_semana": None,
                    "numero_mes": mes,
                }
            )
    return resultados