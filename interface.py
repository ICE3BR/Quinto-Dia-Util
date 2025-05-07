import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils import calcular_quinto_dia_util, calcular_quintos_dias_util_ano_completo, formatar_data_extenso
import os
import csv
from dotenv import load_dotenv

# --- Inicialização da janela principal ---
root = tk.Tk()
root.withdraw()

# Carrega variáveis do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
token = os.getenv("API_TOKEN")
if not token:
    messagebox.showerror("Erro", "Token da API não encontrado no .env.", parent=root)
    root.destroy()
    exit()

# Variáveis de controle
uf_var = tk.StringVar()
ano_var = tk.StringVar()
mes_var = tk.StringVar()
sabado_var = tk.BooleanVar()
todos_var = tk.BooleanVar()
resultado_dados = []

# Força uppercase no UF
uf_var.trace_add('write', lambda *args: uf_var.set(uf_var.get().upper()))

def toggle_mes_entry():
    mes_entry.configure(state='disabled' if todos_var.get() else 'normal')

# Função de cálculo
def calcular():
    global resultado_dados
    resultado_dados = []

    uf = uf_var.get().strip()
    ano_str = ano_var.get().strip()
    contar_sab = sabado_var.get()
    calc_ano = todos_var.get()
    mes_str = mes_var.get().strip()

    # Validações
    if len(uf) != 2 or not uf.isalpha():
        messagebox.showwarning("Entrada inválida", "Informe a UF com 2 letras.", parent=root)
        return
    try:
        ano = int(ano_str)
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Ano inválido.", parent=root)
        return

    # Monta resultado
    text = ""
    if calc_ano:
        resultados = calcular_quintos_dias_util_ano_completo(ano, uf, token, contar_sab)
        resultado_dados = resultados
        for item in resultados:
            mes_nome = item['mes']
            num = item['numero_mes']
            data = item['data'] or 'Menos de 5 dias úteis'
            dia_sem = item['dia_semana'] or ''
            text += f"{mes_nome} ({num:02d}/{ano}): {data} ({dia_sem})\n"
    else:
        try:
            mes = int(mes_str)
            if not 1 <= mes <= 12:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Informe um mês válido (1-12).", parent=root)
            return
        dias = calcular_quinto_dia_util(ano, mes, uf, token, contar_sab)
        if len(dias) >= 5:
            data_fmt, dia_sem, mes_nome = formatar_data_extenso(dias[4])
            resultado_dados = [{"mes": mes_nome, "numero_mes": mes, "data": data_fmt, "dia_semana": dia_sem}]
            text = f"O quinto dia útil de {mes_nome} ({mes:02d}/{ano}) em {uf} é {data_fmt} ({dia_sem})."
        else:
            text = f"O mês {mes:02d}/{ano} em {uf} possui apenas {len(dias)} dias úteis:\n"
            for d in dias:
                d_fmt, d_sem, _ = formatar_data_extenso(d)
                text += f" - {d_fmt} ({d_sem})\n"

    resultado_text.config(state='normal')
    resultado_text.delete('1.0', tk.END)
    resultado_text.insert('1.0', text)
    resultado_text.config(state='disabled')
    root.deiconify()

# Função para exportar CSV
def exportar_csv():
    if not resultado_dados:
        messagebox.showwarning("Sem dados", "Realize um cálculo antes de exportar.", parent=root)
        return
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV Files", "*.csv")],
                                        title="Salvar como")
    if path:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['mes','numero_mes','data','dia_semana'])
            writer.writeheader()
            for row in resultado_dados:
                writer.writerow(row)
        messagebox.showinfo("Exportação", f"Arquivo salvo em:\n{path}", parent=root)

# Estilo moderno
style = ttk.Style(root)
style.configure('TLabel', font=('Segoe UI', 10))
style.configure('TEntry', font=('Segoe UI', 10))
style.configure('TCheckbutton', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 10, 'bold'))

# Configuração da janela
root.title("Quinto Dia Útil")
root.geometry("400x440")
root.minsize(400, 440)
root.resizable(True, True)

# Layout principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# Formulário reorganizado
form = ttk.Frame(main_frame)
form.pack(anchor='n', pady=(0, 10))

# Primeiro linha: UF, Ano, Mês
ttk.Label(form, text="UF:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
uf_entry = ttk.Entry(form, width=5, textvariable=uf_var)
uf_entry.grid(row=0, column=1, sticky='w', pady=2)

ttk.Label(form, text="Ano:").grid(row=0, column=2, sticky='e', padx=15, pady=2)
ano_entry = ttk.Entry(form, width=10, textvariable=ano_var)
ano_entry.grid(row=0, column=3, sticky='w', pady=2)

ttk.Label(form, text="Mês:").grid(row=0, column=4, sticky='e', padx=15, pady=2)
mes_entry = ttk.Entry(form, width=10, textvariable=mes_var)
mes_entry.grid(row=0, column=5, sticky='w', pady=2)

# Segunda linha: checkbuttons
ttk.Checkbutton(form, text="Contar sábados", variable=sabado_var).grid(row=1, column=0, columnspan=3, sticky='w', padx=5, pady=5)
ttk.Checkbutton(form, text="Calcular 12 meses", variable=todos_var, command=toggle_mes_entry).grid(row=1, column=3, columnspan=3, sticky='w', padx=5, pady=5)

# Botões
btns = ttk.Frame(main_frame)
btns.pack(pady=10)

ttk.Button(btns, text="Calcular", command=calcular).pack(side='left', padx=5)
ttk.Button(btns, text="Exportar CSV", command=exportar_csv).pack(side='left', padx=5)

# Área de resultado
bg_color = root.cget('bg')
resultado_text = tk.Text(
    main_frame,
    wrap='word',
    font=('Consolas', 10),
    borderwidth=0,
    highlightthickness=0,
    bg=bg_color,
    state='disabled'
)
resultado_text.pack(fill='both', expand=True, padx=5, pady=5)

# Inicializa interface
toggle_mes_entry()
root.deiconify()
root.mainloop()