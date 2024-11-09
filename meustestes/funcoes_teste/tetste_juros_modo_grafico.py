import tkinter as tk
from tkinter import messagebox
from meu_modulo_juros_compostos import juros_compostos

# Função de cálculo sem os prints de conferência
def calcular():
    try:
        # Coletando e convertendo os valores dos campos de entrada
        investimento = float(entry_investimento.get())
        juros = float(entry_juros.get())
        periodo = int(entry_periodo.get())  # Em meses

        # Calculando o montante usando a função do módulo
        montante = juros_compostos(investimento, periodo, juros)

        # Exibindo o resultado na interface
        messagebox.showinfo("Resultado", f"Montante final: R$ {montante:,.2f}")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de Juros Compostos")

# Labels e campos de entrada para Investimento, Juros e Período
tk.Label(root, text="Investimento Inicial (R$):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_investimento = tk.Entry(root)
entry_investimento.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Taxa de Juros (%):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_juros = tk.Entry(root)
entry_juros.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Período (meses):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_periodo = tk.Entry(root)
entry_periodo.grid(row=2, column=1, padx=10, pady=5)

# Botão para calcular
botao_calcular = tk.Button(root, text="Calcular", command=calcular)
botao_calcular.grid(row=3, column=0, columnspan=2, pady=10)

# Inicializa o loop da interface
root.mainloop()
