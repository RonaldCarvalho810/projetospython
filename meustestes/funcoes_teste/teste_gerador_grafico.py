import tkinter as tk
from tkinter import messagebox
import random

def gerar_numeros():
    try:
        primeiro = int(entry_primeiro.get())
        ultimo = int(entry_ultimo.get())
        rodadas = int(entry_rodadas.get())
        quantidade_dezenas = int(entry_dezenas.get())

        if primeiro > ultimo:
            messagebox.showerror("Erro", "O primeiro número deve ser menor ou igual ao último!")
            return

        lista_original = list(range(primeiro, ultimo + 1))
        resultados = []

        for interno1 in range(rodadas):
            lista = lista_original[:]
            dezenas_selecionadas = []

            for _ in range(quantidade_dezenas):
                for interno_rodadas in range(0,rodadas):
                    random.shuffle(lista)
                escolhido = lista.pop(0)
                dezenas_selecionadas.append(escolhido)

            dezenas_selecionadas = sorted(dezenas_selecionadas)
            resultado = f"Rodada {interno1 + 1}: " + " ".join(f"{num:02}" for num in dezenas_selecionadas)
            resultados.append(resultado)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "\n".join(resultados))
        
        # Ajustar altura com base no número de linhas
        linhas = len(resultados)
        output_text.config(height=min(20, linhas + 2))
        
        # Ajustar largura com base no comprimento da maior linha
        largura = max(len(linha) for linha in resultados) + 2  # Margem de segurança
        output_text.config(width=min(80, largura))  # Limitar largura máxima a 80 caracteres
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos!")

def limpar_campos():
    entry_primeiro.delete(0, tk.END)
    entry_ultimo.delete(0, tk.END)
    entry_rodadas.delete(0, tk.END)
    entry_dezenas.delete(0, tk.END)
    output_text.delete("1.0", tk.END)
    output_text.config(height=10, width=50)  # Resetar altura e largura padrão

# Configuração da janela principal
root = tk.Tk()
root.title("Gerador de jogos")
root.configure(bg="black")  # Fundo preto

# Layout dos elementos
frame = tk.Frame(root, padx=10, pady=10, bg="black")
frame.pack()

# Labels e entradas
tk.Label(frame, text="Primeiro número:", bg="black", fg="white").grid(row=0, column=0, sticky="w")
entry_primeiro = tk.Entry(frame)
entry_primeiro.grid(row=0, column=1)

tk.Label(frame, text="Último número:", bg="black", fg="white").grid(row=1, column=0, sticky="w")
entry_ultimo = tk.Entry(frame)
entry_ultimo.grid(row=1, column=1)

tk.Label(frame, text="Quantidade de rodadas:", bg="black", fg="white").grid(row=2, column=0, sticky="w")
entry_rodadas = tk.Entry(frame)
entry_rodadas.grid(row=2, column=1)

tk.Label(frame, text="Quantidade de dezenas:", bg="black", fg="white").grid(row=3, column=0, sticky="w")
entry_dezenas = tk.Entry(frame)
entry_dezenas.grid(row=3, column=1)

# Botões
btn_gerar = tk.Button(frame, text="Gerar", command=gerar_numeros, bg="white", fg="black")
btn_gerar.grid(row=4, column=0, pady=10)

btn_limpar = tk.Button(frame, text="Limpar", command=limpar_campos, bg="white", fg="black")
btn_limpar.grid(row=4, column=1, pady=10)

# Caixa de texto para saída
output_text = tk.Text(root, height=10, width=50, wrap="word", bg="black", fg="white")
output_text.pack(padx=10, pady=10)

# Executar a interface gráfica
root.mainloop()
