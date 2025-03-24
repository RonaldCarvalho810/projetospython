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


# Tela de Cadastro Genérica
def abrir_cadastro(titulo, tabela, campos):
    janela = tk.Toplevel()
    janela.title(f"Cadastro de {titulo}")
    janela.geometry("800x450")
    configurar_tema(janela)

    entradas = {}
    for i, campo in enumerate(campos):
        ttk.Label(janela, text=f"{campo.capitalize()}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = ttk.Entry(janela, width=30)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        entradas[campo] = entrada

    colunas = list(campos)
    grade = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
    grade.grid(row=len(campos), column=0, columnspan=3, padx=10, pady=10)

    for col in colunas:
        grade.heading(col, text=col.capitalize())
        grade.column(col, width=150, anchor="center")

    def atualizar_grade():
        for item in grade.get_children():
            grade.delete(item)
        for dado in carregar_dados(tabela):
            valores = [dado.get(campo, "") for campo in campos]
            grade.insert("", tk.END, iid=dado["id"], values=valores)

    def salvar_item():
        novo_item = {campo: entradas[campo].get().strip() for campo in campos}
        if not all(novo_item.values()):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        salvar_dado(tabela, novo_item)
        atualizar_grade()
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
        messagebox.showinfo("Sucesso", f"{titulo} cadastrado com sucesso!")

    def excluir_item():
        selecionado = grade.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um item para excluir.")
            return
        item_id = int(selecionado[0])
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (item_id,))
        conexao.commit()
        conexao.close()
        atualizar_grade()
        messagebox.showinfo("Sucesso", f"{titulo} excluído com sucesso!")

    atualizar_grade()
    ttk.Button(janela, text=f"Salvar {titulo}", command=salvar_item).grid(row=len(campos) + 1, column=0, pady=10, sticky="w", padx=10)
    ttk.Button(janela, text="Excluir Selecionado", command=excluir_item).grid(row=len(campos) + 1, column=1, pady=10, sticky="e", padx=10)


# Tela de Agendamentos
def abrir_agendamentos():
    janela = tk.Toplevel()
    janela.title("Agendamentos")
    janela.geometry("800x600")
    configurar_tema(janela)

    clientes = carregar_dados("clientes")
    funcionarios = carregar_dados("funcionarios")
    servicos = carregar_dados("servicos")

    if not clientes or not funcionarios or not servicos:
        messagebox.showerror("Erro", "Cadastre clientes, funcionários e serviços antes de agendar.")
        janela.destroy()
        return

    ttk.Label(janela, text="Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    cliente_combo = ttk.Combobox(janela, values=[c['nome'] for c in clientes], state="readonly", width=30)
    cliente_combo.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(janela, text="Serviço:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    servico_combo = ttk.Combobox(janela, values=[s['nome'] for s in servicos], state="readonly", width=30)
    servico_combo.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(janela, text="Funcionário:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    funcionario_combo = ttk.Combobox(janela, values=[f['nome'] for f in funcionarios], state="readonly", width=30)
    funcionario_combo.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(janela, text="Data (dd/mm/aaaa):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entrada_data = ttk.Entry(janela, width=30)
    entrada_data.grid(row=3, column=1, padx=10, pady=5)

    colunas = ("cliente", "servico", "funcionario", "data")
    grade = ttk.Treeview(janela, columns=colunas, show="headings", height=15)
    grade.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    for col in colunas:
        grade.heading(col, text=col.capitalize())
        grade.column(col, width=150, anchor="center")

    def atualizar_grade():
        for item in grade.get_children():
            grade.delete(item)
        for agendamento in carregar_dados("agendamentos"):
            grade.insert("", tk.END, iid=agendamento["id"], values=(agendamento["cliente"], agendamento["servico"], agendamento["funcionario"], agendamento["data"]))

    def salvar_agendamento():
        cliente = cliente_combo.get()
        servico = servico_combo.get()
        funcionario = funcionario_combo.get()
        data = entrada_data.get().strip()
        if not cliente or not servico or not funcionario or not data:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        salvar_dado("agendamentos", {"cliente": cliente, "servico": servico, "funcionario": funcionario, "data": data})
        atualizar_grade()
        cliente_combo.set("")
        servico_combo.set("")
        funcionario_combo.set("")
        entrada_data.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Agendamento salvo com sucesso!")

    def excluir_agendamento():
        selecionado = grade.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um agendamento para excluir.")
            return
        item_id = int(selecionado[0])
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ?", (item_id,))
        conexao.commit()
        conexao.close()
        atualizar_grade()
        messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso!")

    atualizar_grade()
    ttk.Button(janela, text="Salvar Agendamento", command=salvar_agendamento).grid(row=4, column=0, pady=10)
    ttk.Button(janela, text="Excluir Selecionado", command=excluir_agendamento).grid(row=4, column=1, pady=10)


# Tela Principal
def criar_tela_principal():
    inicializar_bd()
    root = tk.Tk()
    root.title("Sistema de Gerenciamento")
    root.geometry("800x600")
    configurar_tema(root)

    ttk.Button(root, text="Clientes", command=lambda: abrir_cadastro("Clientes", "clientes", ["nome", "telefone", "email", "endereco"])).pack(pady=20)
    ttk.Button(root, text="Funcionários", command=lambda: abrir_cadastro("Funcionários", "funcionarios", ["nome", "telefone", "cargo"])).pack(pady=20)
    ttk.Button(root, text="Serviços", command=lambda: abrir_cadastro("Serviços", "servicos", ["nome", "descricao", "preco"])).pack(pady=20)
    ttk.Button(root, text="Agendamentos", command=abrir_agendamentos).pack(pady=20)
    ttk.Button(root, text="Sair", command=root.destroy).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    criar_tela_principal()
