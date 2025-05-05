import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils import calcular_quinto_dia_util, calcular_quintos_dias_util_ano_completo, formatar_data_extenso
import os
import csv
from dotenv import load_dotenv

# --- Inicialização da janela principal ---
root = tk.Tk()
root.withdraw()  # Oculta até configuração completa

# Carrega .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
token = os.getenv("API_TOKEN")
if not token:
    messagebox.showerror("Erro", "Token da API não encontrado no .env.", parent=root)
    root.destroy()
    exit()

# Variáveis de controle
token  # verifica token já carregado
uf_var = tk.StringVar()
ano_var = tk.StringVar()
mes_var = tk.StringVar()
sabado_var = tk.BooleanVar()
todos_var = tk.BooleanVar()
resultado_dados = []

# Força uppercase em UF
def on_uf_change(*args):
    uf_var.set(uf_var.get().upper())
uf_var.trace_add('write', on_uf_change)

# Função para cálculo
def calcular():
    global resultado_dados
    resultado_dados = []

    uf = uf_var.get().strip()
    ano = ano_var.get().strip()
    contar_sabado = sabado_var.get()
    calcular_ano = todos_var.get()
    mes = mes_var.get().strip()

    # Validações básicas
    if not uf or len(uf) != 2:
        messagebox.showwarning("Entrada inválida", "Informe a UF com 2 letras.", parent=root)
        return
    try:
        ano = int(ano)
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Ano inválido.", parent=root)
        return

    # Monta resultado
    result_str = ""
    if calcular_ano:
        resultados = calcular_quintos_dias_util_ano_completo(ano, uf, token, contar_sabado)
        resultado_dados = resultados
        for item in resultados:
            linha = (f"{item['mes']} ({item['numero_mes']:02d}/{ano}): "
                     f"{item['data'] or 'Menos de 5 dias úteis'} "
                     f"({item['dia_semana'] or ''})")
            result_str += linha + "\n"
    else:
        try:
            m = int(mes)
            if not 1 <= m <= 12:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Informe um mês válido entre 1 e 12.", parent=root)
            return
        dias_uteis = calcular_quinto_dia_util(ano, m, uf, token, contar_sabado)
        if len(dias_uteis) >= 5:
            data_fmt, dia_semana, nome_mes = formatar_data_extenso(dias_uteis[4])
            resultado_dados = [{"mes": nome_mes, "numero_mes": m, "data": data_fmt, "dia_semana": dia_semana}]
            result_str = f"O quinto dia útil de {nome_mes} ({m:02d}/{ano}) em {uf} é {data_fmt} ({dia_semana})."
        else:
            result_str = f"O mês {m:02d}/{ano} em {uf} possui apenas {len(dias_uteis)} dias úteis:\n"
            for d in dias_uteis:
                data_fmt, dia_semana, _ = formatar_data_extenso(d)
                result_str += f" - {data_fmt} ({dia_semana})\n"

    # Exibe resultado
    resultado_msg.config(text=result_str)
    root.deiconify()

# Função para exportar CSV
def exportar_csv():
    if not resultado_dados:
        messagebox.showwarning("Sem dados", "Realize um cálculo antes de exportar.", parent=root)
        return
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Salvar como"
    )
    if filepath:
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['mes','numero_mes','data','dia_semana'])
            writer.writeheader()
            for row in resultado_dados:
                writer.writerow(row)
        messagebox.showinfo("Exportação", f"Arquivo salvo em:\n{filepath}", parent=root)

# Habilita/desabilita campo Mês
def toggle_mes_entry():
    state = 'normal' if not todos_var.get() else 'disabled'
    mes_entry.configure(state=state)

# Estilo moderno
style = ttk.Style(root)
style.configure('TLabel', font=('Segoe UI', 10))
style.configure('TEntry', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 10, 'bold'))
style.configure('TCheckbutton', font=('Segoe UI', 10))

# Configurações da janela
root.title("Quinto Dia Útil")
root.geometry("600x440")
root.resizable(False, False)

# Frame principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# Formulário central
form = ttk.Frame(main_frame)
form.pack(anchor='center')

ttk.Label(form, text="UF:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
mesgn = ttk.Entry(form, width=5, textvariable=uf_var)
mesgn.grid(row=0, column=1)

ttk.Label(form, text="Ano:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
ano_entry = ttk.Entry(form, width=10, textvariable=ano_var)
ano_entry.grid(row=1, column=1)

ttk.Checkbutton(form, text="Contar sábados", variable=sabado_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=5)

ttk.Checkbutton(form, text="Calcular 12 meses", variable=todos_var, command=toggle_mes_entry).grid(row=3, column=0, columnspan=2, sticky='w', padx=5)

ttk.Label(form, text="Mês:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
mes_entry = ttk.Entry(form, width=10, textvariable=mes_var)
mes_entry.grid(row=4, column=1)

# Botões de ação
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Calcular", command=calcular).pack(side='left', padx=5)
ttk.Button(btn_frame, text="Exportar CSV", command=exportar_csv).pack(side='left', padx=5)

# Resultado sem caixa branca
resultado_msg = tk.Message(main_frame, text="", font=('Consolas',10), width=560, justify='left')
resultado_msg.pack(fill='both', expand=True, padx=5, pady=10)

# Exibe janela
toggle_mes_entry()
root.deiconify()
root.mainloop()
