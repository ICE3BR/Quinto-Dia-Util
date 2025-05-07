import csv
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from utils import (
    calcular_quinto_dia_util,
    calcular_quintos_dias_util_ano_completo,
    formatar_data_extenso,
    formatar_data_feriado,
    listar_feriados,
)

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

    while True:
        opcao_input = input("Escolha uma opção: [1] Calcular quinto dia útil [2] Listar feriados [3] Calcular todos os quintos dias úteis: ").strip()
        if opcao_input in ["1", "2", "3"]:
            opcao = opcao_input
            break
        print("Opção inválida. Digite 1, 2 ou 3.")

    if opcao == "3":
        return estado, ano, contar_sabado, "12", None, opcao
    else:
        while True:
            try:
                mes = int(input("Informe um mês (1 a 12): "))
                if 1 <= mes <= 12:
                    return estado, ano, contar_sabado, "1", mes, opcao
                else:
                    print("Mês fora do intervalo válido.")
            except ValueError:
                print("Digite um número inteiro para o mês.")


def exportar_csv(dados, ano, estado):
    nome_arquivo = f"quintos_dias_uteis_{estado}_{ano}.csv"
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["mes", "numero_mes", "data", "dia_semana"]
        )
        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso.")


def exportar_feriados_csv(feriados, ano, estado):
    nome_arquivo = f"feriados_{estado}_{ano}.csv"
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["data", "nome", "tipo", "nivel"]
        )
        writer.writeheader()
        for feriado in feriados:
            data_formatada = formatar_data_feriado(feriado['date'])
            row = {
                "data": data_formatada,
                "nome": feriado['name'],
                "tipo": feriado.get('type', ''),
                "nivel": feriado.get('level', '')
            }
            writer.writerow(row)
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso.")


def exibir_feriados(feriados):
    print(f"\nFeriados encontrados: {len(feriados)}")
    for f in feriados:
        data_formatada = formatar_data_feriado(f['date'])
        nome = f['name']
        tipo = f.get('type', '')
        nivel = f.get('level', '')
        print(f"{data_formatada} - {nome} ({tipo}, {nivel})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Corrige acentuação no Windows

    estado, ano, contar_sabado, opcao_mes, mes, opcao = entrada_usuario()

    if opcao == "1":
        # Calcular quinto dia útil
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
    elif opcao == "2":
        # Listar feriados
        feriados = listar_feriados(ano, estado, token, mes)
        exibir_feriados(feriados)
        exportar_feriados_csv(feriados, ano, estado)
    else:
        # Calcular todos os quintos dias úteis
        resultados = calcular_quintos_dias_util_ano_completo(
            ano, estado, token, contar_sabado
        )
        for item in resultados:
            if item["data"]:
                print(
                    f"{item['mes']} ({item['numero_mes']:02d}/{ano}): {item['data']} ({item['dia_semana']})"
                )
            else:
                print(
                    f"{item['mes']} ({item['numero_mes']:02d}/{ano}): Menos de 5 dias úteis."
                )
        exportar_csv(resultados, ano, estado)