import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

# Caminho do arquivo de dados
ARQUIVO_DADOS = "veiculos.txt"

# Função para carregar os dados do arquivo
def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Função para salvar os dados no arquivo
def salvar_dados(dados):
    try:
        with open(ARQUIVO_DADOS, "w") as f:
            json.dump(dados, f, indent=4, default=str)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar os dados.\n{e}")

# Banco de dados inicializado do arquivo
veiculos = carregar_dados()

# Configurar tema escuro
def configurar_tema_escuro(root):
    style = ttk.Style(root)
    root.configure(bg="#1E1E1E")
    style.theme_use("clam")
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Arial", 10))
    style.configure("TButton", background="#444444", foreground="#FFFFFF", font=("Arial", 10), padding=6)
    style.map("TButton", background=[("active", "#555555")])
    style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333", font=("Arial", 10))
    style.configure("Treeview.Heading", background="#444444", foreground="#FFFFFF", font=("Arial", 10, "bold"))

# Função para calcular o custo do tempo de permanência
def calcular_custo(entrada, valor_hora):
    agora = datetime.now()
    entrada = datetime.fromisoformat(entrada)  # Converte string para datetime
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
        custo = valor_hora  # Valor cheio após 45 minutos

    return minutos, round(custo, 2)

# Atualizar grid de veículos ativos
def atualizar_grid(treeview):
    for item in treeview.get_children():
        treeview.delete(item)

    for placa, dados in veiculos.items():
        if dados["status"] == "ativo":
            entrada = datetime.fromisoformat(dados["entrada"]).strftime("%d/%m/%Y %H:%M:%S")
            treeview.insert("", "end", values=(placa, dados["modelo"], entrada, f"R$ {dados['valor_hora']:.2f}"))

# Entrada de veículos
def abrir_formulario_entrada(treeview):
    form_entrada = tk.Toplevel()
    form_entrada.title("Entrada de Veículos")
    form_entrada.geometry("800x350")
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

        if placa in veiculos and veiculos[placa]["status"] == "ativo":
            messagebox.showerror("Erro", "Este veículo já está ativo no estacionamento.")
            return

        try:
            valor_hora = float(valor_hora)
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido para o valor da hora.")
            return

        veiculos[placa] = {
            "modelo": modelo,
            "valor_hora": valor_hora,
            "entrada": datetime.now().isoformat(),
            "status": "ativo",
        }
        salvar_dados(veiculos)

        messagebox.showinfo("Sucesso", f"Veículo {placa} registrado com sucesso!")
        atualizar_grid(treeview)
        form_entrada.destroy()

    ttk.Button(form_entrada, text="Salvar", command=salvar_entrada).pack(pady=20)
    ttk.Button(form_entrada, text="Fechar", command=form_entrada.destroy).pack(pady=10)

# Saída de veículos
def abrir_formulario_saida(treeview):
    form_saida = tk.Toplevel()
    form_saida.title("Saída de Veículos")
    form_saida.geometry("500x200")
    configurar_tema_escuro(form_saida)

    ttk.Label(form_saida, text="Placa do Veículo:").pack(pady=5)
    entrada_placa = ttk.Entry(form_saida, width=30)
    entrada_placa.pack(pady=5)

    def registrar_saida():
        placa = entrada_placa.get().strip().upper()

        if placa not in veiculos or veiculos[placa]["status"] != "ativo":
            messagebox.showerror("Erro", "Este veículo não está registrado como ativo.")
            return

        entrada = veiculos[placa]["entrada"]
        valor_hora = veiculos[placa]["valor_hora"]
        minutos, custo = calcular_custo(entrada, valor_hora)

        veiculos[placa]["status"] = "inativo"  # Atualizar status do veículo
        salvar_dados(veiculos)

        messagebox.showinfo(
            "Saída Registrada",
            f"Veículo: {placa}\nModelo: {veiculos[placa]['modelo']}\nTempo: {int(minutos)} minutos\n"
            f"Valor a pagar: R${custo:.2f}",
        )
        atualizar_grid(treeview)
        form_saida.destroy()

    ttk.Button(form_saida, text="Registrar Saída", command=registrar_saida).pack(pady=20)
    ttk.Button(form_saida, text="Fechar", command=form_saida.destroy).pack(pady=10)

# Tela principal
def main():
    root = tk.Tk()
    root.title("Gerenciamento de Estacionamento")
    root.geometry("800x600")
    configurar_tema_escuro(root)

    ttk.Label(root, text="Veículos Ativos no Estacionamento", font=("Arial", 14)).pack(pady=10)

    # Treeview para exibir os veículos ativos
    colunas = ("Placa", "Modelo", "Entrada", "Valor Hora")
    treeview = ttk.Treeview(root, columns=colunas, show="headings", height=10)
    for coluna in colunas:
        treeview.heading(coluna, text=coluna)
        treeview.column(coluna, width=140, anchor="center")
    treeview.pack(pady=10, fill="x", expand=True)

    atualizar_grid(treeview)

    # Botões para abrir formulários
    ttk.Button(root, text="Entrada de Veículos", command=lambda: abrir_formulario_entrada(treeview)).pack(pady=5)
    ttk.Button(root, text="Saída de Veículos", command=lambda: abrir_formulario_saida(treeview)).pack(pady=5)
    ttk.Button(root, text="Sair", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
