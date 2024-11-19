#controle de estoque - vexjf
import os
import json
import tkinter as tk
from tkinter import messagebox, ttk

produtos = {
    "001": {"produto": "camisa", "preco": 10.50, "estoque": 100},
    "002": {"produto": "tenis", "preco": 100.70, "estoque": 100},
    "003": {"produto": "calca", "preco": 70.00, "estoque": 100}
}

def salvar_dados(produtos, arquivo="produtos.txt"):
    with open(arquivo, "w") as f:
        json.dump(produtos, f)

def carregar_dados(arquivo="produtos.txt"):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return produtos 

def atualizar_tabela():
    for item in tree.get_children():
        tree.delete(item)
    for codigo, dados in produtos.items():
        tree.insert("", tk.END, values=(codigo, dados['produto'], f"R${dados['preco']:.2f}", dados['estoque']))

def alterar_estoque():
    codigo = entry_codigo.get()
    if codigo in produtos:
        try:
            quantidade = int(entry_quantidade.get())
            novo_estoque = produtos[codigo]["estoque"] + quantidade
            
            if novo_estoque < 0:
                messagebox.showerror("Erro", "O estoque não pode ficar negativo!")
            else:
                produtos[codigo]["estoque"] = novo_estoque
                messagebox.showinfo("Sucesso", f"Estoque atualizado para {novo_estoque} unidades.")
                salvar_dados(produtos)
                atualizar_tabela()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido para a quantidade.")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

produtos = carregar_dados()

janela = tk.Tk()
janela.title("Gerenciador de Produtos - VEXJF")

colunas = ("Código", "Produto", "Preço", "Estoque")
tree = ttk.Treeview(janela, columns=colunas, show="headings", height=8)
for coluna in colunas:
    tree.heading(coluna, text=coluna)
    tree.column(coluna, width=100)
tree.pack(pady=10)

atualizar_tabela()

frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Label(frame, text="Código do Produto:").grid(row=0, column=0, padx=5, pady=5)
entry_codigo = tk.Entry(frame, width=15)
entry_codigo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Quantidade (+/-):").grid(row=1, column=0, padx=5, pady=5)
entry_quantidade = tk.Entry(frame, width=15)
entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

btn_alterar = tk.Button(frame, text="Alterar Estoque", command=alterar_estoque)
btn_alterar.grid(row=2, column=0, columnspan=2, pady=10)

btn_fechar = tk.Button(janela, text="Fechar", command=janela.destroy)
btn_fechar.pack(pady=10)

janela.mainloop()
