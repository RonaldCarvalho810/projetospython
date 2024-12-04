import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DB_PATH = "c:\\banco\\teste.db"

def inicializar_banco():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT UNIQUE,
        endereco TEXT
    )
    """)
    conn.commit()
    conn.close()

def inserir_cliente(nome, telefone, email, endereco):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO clientes (nome, telefone, email, endereco) 
        VALUES (?, ?, ?, ?)
        """, (nome, telefone, email, endereco))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        messagebox.showerror("Erro ao cadastrar", str(e))
        return False
    finally:
        conn.close()

def excluir_cliente(cliente_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def buscar_clientes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def atualizar_grade(grade):
    for item in grade.get_children():
        grade.delete(item)
    for cliente in buscar_clientes():
        grade.insert("", tk.END, values=cliente)

def criar_interface():
    inicializar_banco()

    root = tk.Tk()
    root.title("Gerenciamento de Clientes")
    root.geometry("800x700")
    root.configure(bg="#2E2E2E")

    estilo = ttk.Style(root)
    estilo.theme_use("default")

    estilo.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=25)
    estilo.map("Treeview", background=[("selected", "#5A5A5A")])
    estilo.configure("Treeview.Heading", background="#444444", foreground="white")

    estilo.configure("TLabel", background="#2E2E2E", foreground="white")
    estilo.configure("TButton", background="#444444", foreground="white", borderwidth=1)
    estilo.map("TButton", background=[("active", "#5A5A5A")])

    frame_formulario = tk.Frame(root, bg="#2E2E2E")
    frame_formulario.pack(pady=10)

    ttk.Label(frame_formulario, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_nome = ttk.Entry(frame_formulario, width=30)
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_telefone = ttk.Entry(frame_formulario, width=30)
    entrada_telefone.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_email = ttk.Entry(frame_formulario, width=30)
    entrada_email.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Endereço:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entrada_endereco = ttk.Entry(frame_formulario, width=30)
    entrada_endereco.grid(row=3, column=1, padx=5, pady=5)

    def cadastrar_cliente():
        nome = entrada_nome.get().strip()
        telefone = entrada_telefone.get().strip()
        email = entrada_email.get().strip()
        endereco = entrada_endereco.get().strip()

        if nome and telefone and email and endereco:
            if inserir_cliente(nome, telefone, email, endereco):
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                atualizar_grade(grade)
                entrada_nome.delete(0, tk.END)
                entrada_telefone.delete(0, tk.END)
                entrada_email.delete(0, tk.END)
                entrada_endereco.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    ttk.Button(frame_formulario, text="Cadastrar", command=cadastrar_cliente).grid(row=4, column=0, columnspan=2, pady=10)

    colunas = ("id", "nome", "telefone", "email", "endereco")
    grade = ttk.Treeview(root, columns=colunas, show="headings", height=15)
    grade.pack(pady=10, fill=tk.BOTH, expand=True)

    for coluna in colunas:
        grade.heading(coluna, text=coluna.capitalize())
        grade.column(coluna, width=150, anchor="center")

    def excluir_registro_selecionado():
        selecionado = grade.selection()
        if selecionado:
            cliente_id = grade.item(selecionado[0], "values")[0]
            excluir_cliente(cliente_id)
            atualizar_grade(grade)
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione um cliente para excluir.")

    atualizar_grade(grade)

    ttk.Button(root, text="Excluir Cliente Selecionado", command=excluir_registro_selecionado).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
