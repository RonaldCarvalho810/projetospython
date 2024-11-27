import tkinter as tk
from tkinter import ttk, messagebox
import os

def configurar_tema_escuro(root):
    style = ttk.Style(root)
    root.configure(bg="#1E1E1E") 
    style.theme_use("clam")
    
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Arial", 12))
    style.configure("TButton", background="#444444", foreground="#FFFFFF", font=("Arial", 12), padding=6)
    style.map("TButton", background=[("active", "#555555")])
    style.configure("TEntry", fieldbackground="#333333", foreground="#FFFFFF", font=("Arial", 12), insertcolor="#FFFFFF")
    style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333", font=("Arial", 10))
    style.configure("Treeview.Heading", background="#444444", foreground="#FFFFFF", font=("Arial", 12))

def salvar_em_arquivo(nome_arquivo, dados):
    try:
        with open(nome_arquivo, "a") as arquivo:
            arquivo.write(dados + "\n")
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar os dados.\n{e}")

def abrir_formulario_clientes():
    form_clientes = tk.Toplevel()
    form_clientes.title("Cadastro de Clientes")
    form_clientes.geometry("400x300")
    configurar_tema_escuro(form_clientes)

    ttk.Label(form_clientes, text="Nome:").pack(pady=5)
    entrada_nome = ttk.Entry(form_clientes, width=30)
    entrada_nome.pack(pady=5)

    ttk.Label(form_clientes, text="Telefone:").pack(pady=5)
    entrada_telefone = ttk.Entry(form_clientes, width=30)
    entrada_telefone.pack(pady=5)

    def salvar_cliente():
        nome = entrada_nome.get().strip()
        telefone = entrada_telefone.get().strip()
        if nome and telefone:
            salvar_em_arquivo("clientes.txt", f"Nome: {nome}, Telefone: {telefone}")
            entrada_nome.delete(0, tk.END)
            entrada_telefone.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    ttk.Button(form_clientes, text="Salvar", command=salvar_cliente).pack(pady=20)
    ttk.Button(form_clientes, text="Fechar", command=form_clientes.destroy).pack(pady=10)

def abrir_formulario_servicos():
    form_servicos = tk.Toplevel()
    form_servicos.title("Serviços Oferecidos")
    form_servicos.geometry("400x300")
    configurar_tema_escuro(form_servicos)

    ttk.Label(form_servicos, text="Serviço:").pack(pady=5)
    entrada_servico = ttk.Entry(form_servicos, width=30)
    entrada_servico.pack(pady=5)

    ttk.Label(form_servicos, text="Preço (R$):").pack(pady=5)
    entrada_preco = ttk.Entry(form_servicos, width=30)
    entrada_preco.pack(pady=5)

    def salvar_servico():
        servico = entrada_servico.get().strip()
        preco = entrada_preco.get().strip()
        if servico and preco:
            salvar_em_arquivo("servicos.txt", f"Serviço: {servico}, Preço: R${preco}")
            entrada_servico.delete(0, tk.END)
            entrada_preco.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    ttk.Button(form_servicos, text="Salvar", command=salvar_servico).pack(pady=20)
    ttk.Button(form_servicos, text="Fechar", command=form_servicos.destroy).pack(pady=10)

def carregar_agendamentos(nome_arquivo="agendamentos.txt"):
    if not os.path.exists(nome_arquivo):
        return []
    try:
        with open(nome_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()
        return [linha.strip() for linha in linhas]
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar os dados.\n{e}")
        return []

def abrir_formulario_agendamento():
    form_agendamento = tk.Toplevel()
    form_agendamento.title("Agendamento de Serviços")
    form_agendamento.geometry("800x600")
    configurar_tema_escuro(form_agendamento)

    ttk.Label(form_agendamento, text="Nome do Cliente:").pack(pady=5)
    entrada_cliente = ttk.Entry(form_agendamento, width=30)
    entrada_cliente.pack(pady=5)

    ttk.Label(form_agendamento, text="Serviço:").pack(pady=5)
    entrada_servico = ttk.Entry(form_agendamento, width=30)
    entrada_servico.pack(pady=5)

    ttk.Label(form_agendamento, text="Data (dd/mm/aaaa):").pack(pady=5)
    entrada_data = ttk.Entry(form_agendamento, width=30)
    entrada_data.pack(pady=5)

    tabela = ttk.Treeview(
        form_agendamento, 
        columns=("Cliente", "Serviço", "Data"), 
        show="headings",
        height=10
    )
    tabela.pack(pady=20, fill="both", expand=True)

    tabela.heading("Cliente", text="Cliente")
    tabela.heading("Serviço", text="Serviço")
    tabela.heading("Data", text="Data")
    tabela.column("Cliente", width=200)
    tabela.column("Serviço", width=200)
    tabela.column("Data", width=100)

    def atualizar_tabela():
        tabela.delete(*tabela.get_children())  
        agendamentos = carregar_agendamentos()
        for agendamento in agendamentos:
            dados = agendamento.split(", ")
            if len(dados) == 3:
                tabela.insert("", "end", values=(dados[0][8:], dados[1][8:], dados[2][6:]))

    def salvar_agendamento():
        cliente = entrada_cliente.get().strip()
        servico = entrada_servico.get().strip()
        data = entrada_data.get().strip()
        if cliente and servico and data:
            novo_agendamento = f"Cliente: {cliente}, Serviço: {servico}, Data: {data}"
            salvar_em_arquivo("agendamentos.txt", novo_agendamento)
            entrada_cliente.delete(0, tk.END)
            entrada_servico.delete(0, tk.END)
            entrada_data.delete(0, tk.END)
            atualizar_tabela()  
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    ttk.Button(form_agendamento, text="Salvar", command=salvar_agendamento).pack(pady=10)
    ttk.Button(form_agendamento, text="Fechar", command=form_agendamento.destroy).pack(pady=10)

    atualizar_tabela()

def main():
    root = tk.Tk()
    root.title("Gerenciamento de Serviços")
    root.geometry("400x300")
    configurar_tema_escuro(root)

    ttk.Label(root, text="Selecione uma opção:", font=("Arial", 14)).pack(pady=20)

    ttk.Button(root, text="Cadastro de Clientes", command=abrir_formulario_clientes).pack(pady=10)
    ttk.Button(root, text="Agendamento de Serviços", command=abrir_formulario_agendamento).pack(pady=10)
    ttk.Button(root, text="Serviços Oferecidos", command=abrir_formulario_servicos).pack(pady=10)
    ttk.Button(root, text="Sair", command=root.destroy).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
