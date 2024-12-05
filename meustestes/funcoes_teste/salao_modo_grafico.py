import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Caminho do Banco de Dados
DIRETORIO = "c:\\vexjf"
BANCO = os.path.join(DIRETORIO, "bnc_dds.db")

# Funções para o Banco de Dados
def inicializar_bd():
    # Garantir que o diretório existe
    if not os.path.exists(DIRETORIO):
        os.makedirs(DIRETORIO)

    # Inicializar o banco de dados
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    # Criação das tabelas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        endereco TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        cargo TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        servico TEXT NOT NULL,
        funcionario TEXT NOT NULL,
        data TEXT NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()

def salvar_dado(tabela, dados):
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    campos = ", ".join(dados.keys())
    valores = ", ".join(["?" for _ in dados.values()])
    cursor.execute(f"INSERT INTO {tabela} ({campos}) VALUES ({valores})", list(dados.values()))
    conexao.commit()
    conexao.close()

def carregar_dados(tabela):
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM {tabela}")
    colunas = [desc[0] for desc in cursor.description]
    resultados = cursor.fetchall()
    conexao.close()
    return [dict(zip(colunas, linha)) for linha in resultados]

def excluir_dado(tabela, condicao):
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE {condicao}")
    conexao.commit()
    conexao.close()

# Configurar tema
def configurar_tema(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg="#1E1E1E")
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Arial", 10))
    style.configure("TButton", background="#444444", foreground="#FFFFFF", font=("Arial", 10), padding=6)
    style.map("TButton", background=[("active", "#555555")])
    style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333", font=("Arial", 10))
    style.configure("Treeview.Heading", background="#444444", foreground="#FFFFFF", font=("Arial", 10, "bold"))

# Outras funções mantêm-se iguais (Cadastro, Agendamentos, e Tela Principal)

# Tela Principal
def tela_principal():
    root = tk.Tk()
    root.title("Sistema para Salão de Beleza")
    root.geometry("600x400")
    configurar_tema(root)

    ttk.Button(root, text="Cadastro de Clientes", command=lambda: abrir_cadastro("Cliente", "clientes", ["nome", "telefone", "email", "endereco"])).pack(pady=10)
    ttk.Button(root, text="Cadastro de Funcionários", command=lambda: abrir_cadastro("Funcionário", "funcionarios", ["nome", "telefone", "cargo"])).pack(pady=10)
    ttk.Button(root, text="Cadastro de Serviços", command=lambda: abrir_cadastro("Serviço", "servicos", ["nome", "descricao", "preco"])).pack(pady=10)
    ttk.Button(root, text="Agendamentos", command=abrir_agendamentos).pack(pady=10)
    ttk.Button(root, text="Sair", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    inicializar_bd()
    tela_principal()
