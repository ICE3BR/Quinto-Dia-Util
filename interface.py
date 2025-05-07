import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils import (
    calcular_quinto_dia_util,
    calcular_quintos_dias_util_ano_completo,
    formatar_data_extenso,
    listar_feriados
)
import os
import csv
import threading
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
status_var = tk.StringVar(value="Aguardando...")
resultado_dados = []

# Força uppercase no UF
uf_var.trace_add('write', lambda *args: uf_var.set(uf_var.get().upper()))

def toggle_mes_entry():
    mes_entry.configure(state='disabled' if todos_var.get() else 'normal')

# Define o estado dos botões (ativo/inativo)
def set_botoes_estado(estado):
    calcular_btn.configure(state=estado)
    feriado_btn.configure(state=estado)
    exportar_btn.configure(state=estado)
    
    # Também atualiza estado dos campos de entrada
    uf_entry.configure(state=estado)
    ano_entry.configure(state=estado)
    if not todos_var.get():
        mes_entry.configure(state=estado)

# Atualiza a área de status
def atualizar_status(mensagem, mostrar_progresso=False):
    status_var.set(mensagem)
    if mostrar_progresso:
        progress_bar.pack(fill='x', padx=5, pady=2)
        # Iniciar a animação da barra de progresso
        progress_bar.start(10)  # Velocidade da animação
    else:
        # Parar a animação quando não estiver mostrando
        progress_bar.stop()
        progress_bar.pack_forget()
    root.update_idletasks()

# Função que executa em thread separada para não travar a interface
def executar_tarefa(func, *args):
    # Desabilita os controles durante o processamento
    set_botoes_estado('disabled')
    atualizar_status("Processando...", True)
    
    try:
        resultado = func(*args)
        status_var.set("Concluído")
        return resultado
    except Exception as e:
        status_var.set(f"Erro: {str(e)}")
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}", parent=root)
        return None
    finally:
        # Reativa controles após o processamento
        progress_bar.pack_forget()
        set_botoes_estado('normal')

# Calcula quinto dia útil
def calcular_quinto():
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

    if not calc_ano:
        try:
            mes = int(mes_str)
            if not 1 <= mes <= 12:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Informe um mês válido (1-12).", parent=root)
            return
    
    # Inicia thread de processamento
    def processar():
        nonlocal uf, ano, contar_sab, calc_ano, mes_str
        ano = int(ano_str)
        
        if calc_ano:
            resultados = executar_tarefa(
                calcular_quintos_dias_util_ano_completo,
                ano, uf, token, contar_sab
            )
            if resultados:
                resultado_dados = resultados
                text = ""
                for item in resultados:
                    mes_nome = item['mes']
                    num = item['numero_mes']
                    data = item['data'] or 'Menos de 5 dias úteis'
                    dia_sem = item['dia_semana'] or ''
                    text += f"{mes_nome} ({num:02d}/{ano}): {data} ({dia_sem})\n"
                
                # Atualiza a interface na thread principal
                root.after(0, lambda: atualizar_resultado_text(text))
        else:
            mes = int(mes_str)
            dias = executar_tarefa(
                calcular_quinto_dia_util,
                ano, mes, uf, token, contar_sab
            )
            if dias:
                if len(dias) >= 5:
                    data_fmt, dia_sem, mes_nome = formatar_data_extenso(dias[4])
                    resultado_dados = [{"mes": mes_nome, "numero_mes": mes, "data": data_fmt, "dia_semana": dia_sem}]
                    text = f"O quinto dia útil de {mes_nome} ({mes:02d}/{ano}) em {uf} é {data_fmt} ({dia_sem})."
                else:
                    text = f"O mês {mes:02d}/{ano} em {uf} possui apenas {len(dias)} dias úteis:\n"
                    for d in dias:
                        d_fmt, d_sem, _ = formatar_data_extenso(d)
                        text += f" - {d_fmt} ({d_sem})\n"
                
                # Atualiza a interface na thread principal
                root.after(0, lambda: atualizar_resultado_text(text))
    
    # Inicia a thread
    thread = threading.Thread(target=processar)
    thread.daemon = True
    thread.start()
    root.deiconify()

def atualizar_resultado_text(texto):
    resultado_text.config(state='normal')
    resultado_text.delete('1.0', tk.END)
    resultado_text.insert('1.0', texto)
    resultado_text.config(state='disabled')

def formatar_data_feriado(data_iso):
    """
    Converte data no formato ISO (YYYY-MM-DD) para o formato DD/MM/YYYY
    """
    partes = data_iso.split('-')
    if len(partes) == 3:
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
    return data_iso  # Retorna o original se não conseguir formatar

# Calcula feriados para mês ou ano
def calcular_feriado():
    uf = uf_var.get().strip()
    ano_str = ano_var.get().strip()
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

    if not calc_ano:
        try:
            mes = int(mes_str)
            if not 1 <= mes <= 12:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Informe um mês válido (1-12).", parent=root)
            return
    
    # Inicia thread de processamento
    def processar():
        nonlocal uf, ano, calc_ano, mes_str
        
        if calc_ano:
            feriados = executar_tarefa(listar_feriados, ano, uf, token)
        else:
            mes = int(mes_str)
            feriados = executar_tarefa(listar_feriados, ano, uf, token, mes)
        
        if feriados:
            # Monta texto com data formatada
            text = ""
            for f in feriados:
                date_iso = f['date']
                date_formatted = formatar_data_feriado(date_iso)
                name = f['name']
                type_ = f.get('type', '')
                level = f.get('level', '')
                text += f"{date_formatted} - {name} ({type_}, {level})\n"
            if not text:
                text = "Nenhum feriado encontrado."
            
            # Atualiza a interface na thread principal
            root.after(0, lambda: atualizar_resultado_text(text))
    
    # Inicia a thread
    thread = threading.Thread(target=processar)
    thread.daemon = True
    thread.start()
    root.deiconify()

# Função para exportar CSV
def exportar_csv():
    if not resultado_dados:
        messagebox.showwarning("Sem dados", "Realize um cálculo antes de exportar.", parent=root)
        return
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV Files", "*.csv")], title="Salvar como")
    if path:
        try:
            atualizar_status("Exportando para CSV...", True)
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['mes','numero_mes','data','dia_semana'])
                writer.writeheader()
                for row in resultado_dados:
                    writer.writerow(row)
            messagebox.showinfo("Exportação", f"Arquivo salvo em:\n{path}", parent=root)
            atualizar_status("CSV exportado com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}", parent=root)
            atualizar_status(f"Erro ao exportar: {str(e)}")
        finally:
            progress_bar.pack_forget()

# Estilo moderno
style = ttk.Style(root)
style.configure('TLabel', font=('Segoe UI', 10))
style.configure('TEntry', font=('Segoe UI', 10))
style.configure('TCheckbutton', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 10, 'bold'))

# Configuração da janela
root.title("Quinto Dia Útil")
root.geometry("615x480")
root.minsize(615, 480)
root.resizable(True, True)

# Layout principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# Formulário reorganizado com UF, Ano, Mês em linha única
form = ttk.Frame(main_frame)
form.pack(anchor='n', pady=(0, 10))

ttk.Label(form, text="UF:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
uf_entry = ttk.Entry(form, width=5, textvariable=uf_var)
uf_entry.grid(row=0, column=1, sticky='w', pady=2)

ttk.Label(form, text="Ano:").grid(row=0, column=2, sticky='e', padx=15, pady=2)
ano_entry = ttk.Entry(form, width=10, textvariable=ano_var)
ano_entry.grid(row=0, column=3, sticky='w', pady=2)

ttk.Label(form, text="Mês:").grid(row=0, column=4, sticky='e', padx=15, pady=2)
mes_entry = ttk.Entry(form, width=10, textvariable=mes_var)
mes_entry.grid(row=0, column=5, sticky='w', pady=2)

# Checkboxes
ttk.Checkbutton(form, text="Contar sábados", variable=sabado_var).grid(row=1, column=0, columnspan=3, sticky='w', padx=5, pady=5)
ttk.Checkbutton(form, text="Calcular 12 meses", variable=todos_var, command=toggle_mes_entry).grid(row=1, column=3, columnspan=3, sticky='w', padx=5, pady=5)

# Botões de ação
btns = ttk.Frame(main_frame)
btns.pack(pady=10)

calcular_btn = ttk.Button(btns, text="Calcular Quinto-Dia-Util", command=calcular_quinto)
calcular_btn.pack(side='left', padx=5)

feriado_btn = ttk.Button(btns, text="Calcular Feriado", command=calcular_feriado)
feriado_btn.pack(side='left', padx=5)

exportar_btn = ttk.Button(btns, text="Exportar CSV", command=exportar_csv)
exportar_btn.pack(side='left', padx=5)

# Frame de status logo abaixo dos botões e acima do resultado
status_frame = ttk.Frame(main_frame)
status_frame.pack(fill='x', pady=(5, 10))

# Label de status
status_label = ttk.Label(status_frame, textvariable=status_var, anchor='w')
status_label.pack(side='left', fill='x', padx=(0, 10))

# Barra de progresso 
progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
progress_bar.pack(side='right', fill='x', expand=True)
progress_bar.pack_forget()  # Inicialmente escondida

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