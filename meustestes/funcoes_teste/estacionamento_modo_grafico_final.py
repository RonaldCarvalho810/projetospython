import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
import os

# Configuração do caminho do banco de dados
PASTA_BANCO = r"C:\vexjf"
BANCO_DADOS = os.path.join(PASTA_BANCO, "bnc_dds_estacionamento.bd")

# Função para inicializar o banco de dados
def inicializar_banco():
    if not os.path.exists(PASTA_BANCO):
        os.makedirs(PASTA_BANCO)

    conexao = sqlite3.connect(BANCO_DADOS)
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        placa TEXT PRIMARY KEY,
        modelo TEXT NOT NULL,
        valor_hora REAL NOT NULL,
        entrada TEXT,
        status TEXT NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()

# Funções de manipulação de dados no banco
def executar_query(query, parametros=()):
    conexao = sqlite3.connect(BANCO_DADOS)
    cursor = conexao.cursor()
    cursor.execute(query, parametros)
    conexao.commit()
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def carregar_veiculos():
    return executar_query("SELECT * FROM veiculos WHERE status = 'ativo'")

# Configuração de tema escuro
def configurar_tema_escuro(root):
    style = ttk.Style(root)
    root.configure(bg="#1E1E1E")
    style.theme_use("clam")
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Arial", 10))
    style.configure("TButton", background="#444444", foreground="#FFFFFF", font=("Arial", 10), padding=6)
    style.map("TButton", background=[("active", "#555555")])
    style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333", font=("Arial", 10))
    style.configure("Treeview.Heading", background="#444444", foreground="#FFFFFF", font=("Arial", 10, "bold"))

def calcular_custo(entrada, valor_hora):
    agora = datetime.now()
    entrada = datetime.fromisoformat(entrada)
    delta = agora - entrada
    minutos = delta.total_seconds() / 60
    valor_minuto = valor_hora / 60

    if minutos <= 15:
        custo = valor_minuto * 15
    elif minutos <= 30:
        custo = valor_minuto * 30
    elif minutos <= 45:
        custo = valor_minuto * 45
    else:
        custo = valor_hora

    return minutos, round(custo, 2)

def atualizar_grid(treeview):
    for item in treeview.get_children():
        treeview.delete(item)

    veiculos = carregar_veiculos()
    for placa, modelo, valor_hora, entrada, status in veiculos:
        entrada_formatada = datetime.fromisoformat(entrada).strftime("%d/%m/%Y %H:%M:%S")
        treeview.insert("", "end", values=(placa, modelo, entrada_formatada, f"R$ {valor_hora:.2f}"))

def abrir_formulario_entrada(treeview):
    form_entrada = tk.Toplevel()
    form_entrada.title("Entrada de Veículos")
    form_entrada.geometry("400x300")
    configurar_tema_escuro(form_entrada)

    ttk.Label(form_entrada, text="Placa do Veículo:").pack(pady=5)
    entrada_placa = ttk.Entry(form_entrada, width=30)
    entrada_placa.pack(pady=5)

    ttk.Label(form_entrada, text="Modelo:").pack(pady=5)
    entrada_modelo = ttk.Entry(form_entrada, width=30)
    entrada_modelo.pack(pady=5)

    ttk.Label(form_entrada, text="Valor da Hora (R$):").pack(pady=5)
    entrada_valor_hora = ttk.Entry(form_entrada, width=30)
    entrada_valor_hora.pack(pady=5)

    def salvar_entrada():
        placa = entrada_placa.get().strip().upper()
        modelo = entrada_modelo.get().strip()
        valor_hora = entrada_valor_hora.get().strip()

        if not placa or not modelo or not valor_hora:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        try:
            valor_hora = float(valor_hora)
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido para o valor da hora.")
            return

        try:
            executar_query("""
            INSERT INTO veiculos (placa, modelo, valor_hora, entrada, status)
            VALUES (?, ?, ?, ?, ?)
            """, (placa, modelo, valor_hora, datetime.now().isoformat(), "ativo"))

            messagebox.showinfo("Sucesso", f"Veículo {placa} registrado com sucesso!")
            atualizar_grid(treeview)
            form_entrada.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este veículo já está registrado.")

    ttk.Button(form_entrada, text="Salvar", command=salvar_entrada).pack(pady=20)
    ttk.Button(form_entrada, text="Fechar", command=form_entrada.destroy).pack(pady=10)

def abrir_formulario_saida(treeview, placa=None):
    form_saida = tk.Toplevel()
    form_saida.title("Saída de Veículos")
    form_saida.geometry("400x300")
    configurar_tema_escuro(form_saida)

    ttk.Label(form_saida, text="Placa do Veículo:").pack(pady=5)
    entrada_placa = ttk.Entry(form_saida, width=30)
    entrada_placa.pack(pady=5)

    if placa:
        entrada_placa.insert(0, placa)
        entrada_placa.config(state="readonly")

    def registrar_saida():
        placa = entrada_placa.get().strip().upper()

        veiculo = executar_query("""
        SELECT modelo, valor_hora, entrada FROM veiculos
        WHERE placa = ? AND status = 'ativo'
        """, (placa,))

        if not veiculo:
            messagebox.showerror("Erro", "Este veículo não está registrado como ativo.")
            return

        modelo, valor_hora, entrada = veiculo[0]
        minutos, custo = calcular_custo(entrada, valor_hora)

        executar_query("""
        UPDATE veiculos
        SET status = 'inativo'
        WHERE placa = ?
        """, (placa,))

        messagebox.showinfo(
            "Saída Registrada",
            f"Veículo: {placa}\nModelo: {modelo}\nTempo: {int(minutos)} minutos\n"
            f"Valor a pagar: R${custo:.2f}",
        )
        atualizar_grid(treeview)
        form_saida.destroy()

    ttk.Button(form_saida, text="Registrar Saída", command=registrar_saida).pack(pady=20)
    ttk.Button(form_saida, text="Fechar", command=form_saida.destroy).pack(pady=10)

def main():
    inicializar_banco()
    root = tk.Tk()
    root.title("Gerenciamento de Estacionamento")
    root.geometry("600x400")
    configurar_tema_escuro(root)

    ttk.Label(root, text="Veículos Ativos no Estacionamento", font=("Arial", 14)).pack(pady=10)

    colunas = ("Placa", "Modelo", "Entrada", "Valor Hora")
    treeview = ttk.Treeview(root, columns=colunas, show="headings", height=10)
    for coluna in colunas:
        treeview.heading(coluna, text=coluna)
        treeview.column(coluna, width=140, anchor="center")
    treeview.pack(pady=10, fill="x", expand=True)

    atualizar_grid(treeview)

    def on_double_click(event):
        item = treeview.selection()
        if item:
            placa = treeview.item(item, "values")[0]
            abrir_formulario_saida(treeview, placa)

    treeview.bind("<Double-1>", on_double_click)

    frame_botoes = ttk.Frame(root)
    frame_botoes.pack(pady=10)

    ttk.Button(frame_botoes, text="Entrada de Veículos", command=lambda: abrir_formulario_entrada(treeview)).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Saída de Veículos", command=lambda: abrir_formulario_saida(treeview)).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Sair", command=root.destroy).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()
