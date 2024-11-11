import tkinter as tk
from tkinter import messagebox

# Importando a função de cálculo de juros compostos do módulo
from meu_modulo_juros_compostos import juros_compostos

# Função de cálculo com validação de entrada
def calcular():
    try:
        # Coleta os valores dos campos de entrada
        investimento = float(entry_investimento.get())
        juros = float(entry_juros.get())  # Converte a taxa de juros para decimal
        periodo = int(entry_periodo.get())

        # Chama a função do módulo para calcular os juros compostos
        montante = juros_compostos(investimento, juros, periodo)
        
        # Exibe o resultado em uma caixa de mensagem
        messagebox.showinfo("Resultado", f"Montante final: R$ {montante:.2f}")

    except ValueError:
        # Exibe uma mensagem de erro se a entrada for inválida
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

tk.Label(root, text="Período (anos):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_periodo = tk.Entry(root)
entry_periodo.grid(row=2, column=1, padx=10, pady=5)

# Botão para calcular
botao_calcular = tk.Button(root, text="Calcular", command=calcular)
botao_calcular.grid(row=3, column=0, columnspan=2, pady=10)

# Inicializa o loop da interface
root.mainloop()
