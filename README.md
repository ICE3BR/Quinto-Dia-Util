# Quinto Dia Útil

Projeto em Python para calcular o quinto dia útil de um mês, considerando feriados nacionais e estaduais brasileiros. Pode ser usado para prever datas de pagamento de salários.

## 🧰 Tecnologias Utilizadas

- Python 3.10+
- `requests`
- `python-dotenv`
- `pytest` (para testes)

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

Execute o programa principal:

```bash
python main.py
```

### Entradas do usuário:
1. Estado (UF)
2. Ano (ex: 2025)
3. Contar sábados? [Y/N]
4. Calcular 12 meses? [Y/N]
5. Se não, informe o mês (1-12)

### Exemplo de saída:
```
O quinto dia útil de Março (03/2025) em SP é 07/03/2025 (Sexta-feira).
```

Se optar por calcular os 12 meses, será gerado também um arquivo CSV com os resultados:
```
quintos_dias_uteis_SP_2025.csv
```

## ✅ Testes Automatizados

Para rodar os testes com `pytest`:

```bash
python test_utils.py
```

Todos os testes são executáveis diretamente e utilizam mocks para feriados.

## 📁 Estrutura do Projeto

```
├── main.py              # Entrada do usuário e execução principal
├── utils.py             # Lógica de cálculo e formatação de datas
├── test_utils.py        # Testes automatizados com pytest
├── .env                 # Contém o token da API (não versionar)
├── .env.example         # Exemplo de estrutura do .env
├── requirements.txt     # Dependências do projeto
└── README.md            # Instruções e informações do projeto
```

---

Feito com ❤️ para auxiliar no planejamento financeiro e RH. 

Sugestões e melhorias são bem-vindas!