# Quinto Dia Útil

Aplicação em Python para calcular o quinto dia útil de um mês, considerando feriados nacionais e estaduais brasileiros. Útil para prever datas de pagamento de salários, planejamento financeiro e RH.

## 🧰 Tecnologias Utilizadas

- Python 3.10+
- Tkinter (interface gráfica)
- `requests`
- `python-dotenv`
- `pytest` (para testes)
- Threading (para processos em background)

## 💻 Recursos da Aplicação

- Cálculo do quinto dia útil por mês ou do ano completo
- Listagem de feriados nacionais e estaduais
- Formatação de datas no padrão brasileiro (DD/MM/AAAA)
- Exportação de resultados para CSV
- Interface gráfica intuitiva com feedback visual de processamento
- Suporte a todos os estados brasileiros
- Opção para incluir sábados como dias úteis

## 📦 Instalação

Clone o repositório e instale as dependências:

```bash
uv pip install -r requirements.txt
```

Crie um arquivo `.env` com seu token da API:

```env
API_TOKEN=seu_token_aqui
```

Você pode usar a API da [Invertexto](https://invertexto.com/feriados) para obter o token.

## ▶️ Como Usar

### Modo Interface Gráfica

Execute o módulo de interface:

```bash
python interface.py
```

Na interface gráfica, você pode:
1. Selecionar o estado (UF)
2. Informar o ano
3. Informar o mês (opcional se selecionar "Calcular 12 meses")
4. Marcar a opção para contar sábados
5. Escolher entre calcular um mês específico ou todos os meses
6. Visualizar o quinto dia útil ou listar feriados
7. Exportar os resultados para CSV

### Modo Linha de Comando

Execute o programa principal:

```bash
python main.py
```

Siga as instruções para:
1. Informar o estado (UF)
2. Informar o ano (ex: 2025)
3. Definir se deseja contar sábados [Y/N]
4. Escolher entre calcular quinto dia útil, listar feriados ou calcular todos os meses
5. Informar o mês (1-12) quando necessário

### Exemplo de saída:
```
O quinto dia útil de Março (03/2025) em SP é 07/03/2025 (Sexta-feira).
```

## 📊 Exportação de Dados

Dois tipos de arquivos CSV podem ser gerados:

1. **Quintos dias úteis**:
   - Nome do arquivo: `quintos_dias_uteis_[UF]_[ANO].csv`
   - Colunas: mes, numero_mes, data, dia_semana

2. **Feriados**:
   - Nome do arquivo: `feriados_[UF]_[ANO].csv`
   - Colunas: data, nome, tipo, nivel

## 🚀 Versão Executável

O projeto já inclui uma versão executável compilada na pasta `output/interface.exe`.

Para criar uma nova versão executável, você pode usar auto-py-to-exe ou PyInstaller:

```bash
# Instale o auto-py-to-exe
pip install auto-py-to-exe

# Execute o programa
auto-py-to-exe
```

Configurações recomendadas para o executável:
- Script: `interface.py`
- Modo: One Directory
- Console: Window Based (--noconsole)
- Incluir `.env` em Additional Files
- Adicionar hidden imports: tkinter, requests, dotenv, csv, locale, datetime, calendar
- Pasta de saída: `output/`

## ✅ Testes Automatizados

Para rodar os testes com `pytest`:

```bash
python test_utils.py
```

Os testes incluem:
- Cálculo de quinto dia útil (com e sem sábados)
- Formatação de datas
- Manipulação de meses com menos de 5 dias úteis

## 📁 Estrutura do Projeto

```
├── interface.py         # Interface gráfica Tkinter
├── main.py              # Versão linha de comando
├── utils.py             # Lógica de cálculo e formatação de datas
├── test_utils.py        # Testes automatizados com pytest
├── .env                 # Contém o token da API (não versionar)
├── .env.example         # Exemplo de estrutura do .env
├── requirements.txt     # Dependências do projeto
├── README.md            # Instruções e informações do projeto
└── output/              # Pasta contendo o executável compilado
    └── interface.exe    # Aplicativo executável
```

## 🔄 Atualizações Recentes

- Adição de interface gráfica com Tkinter
- Implementação de threading para evitar congelamento da interface
- Indicador visual de carregamento durante processamento
- Formatação padrão brasileiro para as datas dos feriados
- Funcionalidade para exportação de CSV de feriados
- Opção para criar versão executável (.exe) do aplicativo

---

Feito com ❤️ para auxiliar no planejamento financeiro e RH. 

Sugestões e melhorias são bem-vindas!