import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Arquivos para armazenamento
ARQUIVO_CLIENTES = "clientes.json"
ARQUIVO_FUNCIONARIOS = "funcionarios.json"
ARQUIVO_SERVICOS = "servicos.json"
ARQUIVO_AGENDAMENTOS = "agendamentos.json"

# Funções para manipulação de dados
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            try:
                dados = json.load(f)
                return dados if isinstance(dados, list) else []
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

# Inicializar dados
clientes = carregar_dados(ARQUIVO_CLIENTES)
funcionarios = carregar_dados(ARQUIVO_FUNCIONARIOS)
servicos = carregar_dados(ARQUIVO_SERVICOS)
agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)

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
def abrir_cadastro(titulo, arquivo, campos):
    janela = tk.Toplevel()
    janela.title(f"Cadastro de {titulo}")
    janela.geometry("600x400")
    configurar_tema(janela)

    dados = carregar_dados(arquivo)

    entradas = {}
    for i, campo in enumerate(campos):
        ttk.Label(janela, text=f"{campo}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = ttk.Entry(janela, width=30)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        entradas[campo] = entrada

    colunas = list(campos)
    grade = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
    grade.grid(row=len(campos), column=0, columnspan=2, padx=10, pady=10)

    for col in colunas:
        grade.heading(col, text=col.capitalize())
        grade.column(col, width=150, anchor="center")

    def atualizar_grade():
        for item in grade.get_children():
            grade.delete(item)
        for dado in dados:
            valores = [dado.get(campo, "") for campo in campos]
            grade.insert("", tk.END, values=valores)

    def salvar_item():
        novo_item = {campo: entradas[campo].get().strip() for campo in campos}

        if not all(novo_item.values()):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        dados.append(novo_item)
        salvar_dados(arquivo, dados)
        atualizar_grade()
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
        messagebox.showinfo("Sucesso", f"{titulo} cadastrado com sucesso!")

    atualizar_grade()

    ttk.Button(janela, text=f"Salvar {titulo}", command=salvar_item).grid(row=len(campos) + 1, column=0, columnspan=2, pady=10)

# Tela de Agendamentos
def abrir_agendamentos():
    janela = tk.Toplevel()
    janela.title("Agendamentos")
    janela.geometry("800x600")
    configurar_tema(janela)

    if not clientes or not funcionarios or not servicos:
        messagebox.showerror("Erro", "Cadastre clientes, funcionários e serviços antes de agendar.")
        janela.destroy()
        return

    ttk.Label(janela, text="Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    cliente_combo = ttk.Combobox(janela, values=[cliente['nome'] for cliente in clientes], state="readonly", width=30)
    cliente_combo.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(janela, text="Serviço:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    servico_combo = ttk.Combobox(janela, values=[servico['nome'] for servico in servicos], state="readonly", width=30)
    servico_combo.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(janela, text="Funcionário:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    funcionario_combo = ttk.Combobox(janela, values=[funcionario['nome'] for funcionario in funcionarios], state="readonly", width=30)
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
        for agendamento in agendamentos:
            grade.insert("", tk.END, values=(agendamento["cliente"], agendamento["servico"], agendamento["funcionario"], agendamento["data"]))

    def salvar_agendamento():
        cliente = cliente_combo.get()
        servico = servico_combo.get()
        funcionario = funcionario_combo.get()
        data = entrada_data.get().strip()

        if not cliente or not servico or not funcionario or not data:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        novo_agendamento = {
            "cliente": cliente,
            "servico": servico,
            "funcionario": funcionario,
            "data": data
        }

        agendamentos.append(novo_agendamento)
        salvar_dados(ARQUIVO_AGENDAMENTOS, agendamentos)
        messagebox.showinfo("Sucesso", "Agendamento salvo com sucesso!")
        atualizar_grade()

        cliente_combo.set("")
        servico_combo.set("")
        funcionario_combo.set("")
        entrada_data.delete(0, tk.END)

    atualizar_grade()

    ttk.Button(janela, text="Salvar Agendamento", command=salvar_agendamento).grid(row=4, column=0, columnspan=3, pady=10)

# Tela Principal
def tela_principal():
    root = tk.Tk()
    root.title("Sistema para Salão de Beleza")
    root.geometry("600x400")
    configurar_tema(root)

    ttk.Button(root, text="Cadastro de Clientes", command=lambda: abrir_cadastro("Cliente", ARQUIVO_CLIENTES, ["nome", "telefone", "email", "endereço"])).pack(pady=10)
    ttk.Button(root, text="Cadastro de Funcionários", command=lambda: abrir_cadastro("Funcionário", ARQUIVO_FUNCIONARIOS, ["nome", "telefone", "cargo"])).pack(pady=10)
    ttk.Button(root, text="Cadastro de Serviços", command=lambda: abrir_cadastro("Serviço", ARQUIVO_SERVICOS, ["nome", "descrição", "preço"])).pack(pady=10)
    ttk.Button(root, text="Agendamentos", command=abrir_agendamentos).pack(pady=10)
    ttk.Button(root, text="Sair", command=root.destroy).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    tela_principal()
