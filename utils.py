import os
from datetime import datetime

from dotenv import load_dotenv
from utils import calcular_quinto_dia_util, formatar_data_extenso

# Carrega variáveis do .env
load_dotenv()
token = os.getenv("API_TOKEN")
if not token:
    raise EnvironmentError("Token da API não encontrado no .env.")


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
        if contar_sabado_input in ["Y", "N"]:
            contar_sabado = contar_sabado_input == "Y"
            break
        print("Opção inválida. Digite Y ou N.")

    return estado, mes, ano, contar_sabado


if __name__ == "__main__":
    estado, mes, ano, contar_sabado = entrada_usuario()
    dias_uteis = calcular_quinto_dia_util(ano, mes, estado, token, contar_sabado)

    if len(dias_uteis) >= 5:
        data_formatada, dia_semana, nome_mes = formatar_data_extenso(dias_uteis[4])
        print(
            f"O quinto dia útil de {nome_mes} ({mes:02d}/{ano}) em {estado} é {data_formatada} ({dia_semana})."
        )
    else:
        print(
            f"Atenção: o mês {mes:02d}/{ano} em {estado} possui apenas {len(dias_uteis)} dia(s) útil(is):"
        )
        for dia in dias_uteis:
            data_formatada, dia_semana, _ = formatar_data_extenso(dia)
            print(f" - {data_formatada} ({dia_semana})")
