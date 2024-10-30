import tkinter as tk
from tkinter import messagebox

def somar():
    try:
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado = valor1 + valor2
        resultado_label.config(text=f"Resultado: {resultado}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas números.")

# Configuração da janela principal
root = tk.Tk()
root.title("Soma de Valores")

# Campo de entrada para o primeiro número
label1 = tk.Label(root, text="Valor 1:")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

# Campo de entrada para o segundo número
label2 = tk.Label(root, text="Valor 2:")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

# Botão para somar os valores
botao_somar = tk.Button(root, text="Somar", command=somar)
botao_somar.pack()

# Rótulo para mostrar o resultado
resultado_label = tk.Label(root, text="Resultado: ")
resultado_label.pack()

# Executa o loop da janela
root.mainloop()
