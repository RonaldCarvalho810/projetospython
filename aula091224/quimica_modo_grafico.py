import tkinter as tk
from tkinter import messagebox

def calcular():
    try:
        c1 = entry_c1.get()
        v1 = entry_v1.get()
        c2 = entry_c2.get()
        v2 = entry_v2.get()

        valores = {
            "C1": float(c1) if c1 else None,
            "V1": float(v1) if v1 else None,
            "C2": float(c2) if c2 else None,
            "V2": float(v2) if v2 else None,
        }

        if list(valores.values()).count(None) != 1:
            messagebox.showerror("Erro", "Apenas um valor deve estar vazio.")
            return

        if valores["C1"] is None:
            valores["C1"] = (valores["C2"] * valores["V2"]) / valores["V1"]
            resultado = f"C1 calculado: {valores['C1']:.2f}"
        elif valores["V1"] is None:
            valores["V1"] = (valores["C2"] * valores["V2"]) / valores["C1"]
            resultado = f"V1 calculado: {valores['V1']:.2f}"
        elif valores["C2"] is None:
            valores["C2"] = (valores["C1"] * valores["V1"]) / valores["V2"]
            resultado = f"C2 calculado: {valores['C2']:.2f}"
        elif valores["V2"] is None:
            valores["V2"] = (valores["C1"] * valores["V1"]) / valores["C2"]
            resultado = f"V2 calculado: {valores['V2']:.2f}"

        for chave, valor in valores.items():
            historico[chave].append(valor)

        messagebox.showinfo("Resultado", resultado)

    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de digitar números válidos.")

def mostrar_historico():
    if any(historico[chave] for chave in historico):
        historico_texto = "\n".join(
            f"Cálculo {i + 1}: C1={historico['C1'][i]:.2f}, "
            f"V1={historico['V1'][i]:.2f}, "
            f"C2={historico['C2'][i]:.2f}, "
            f"V2={historico['V2'][i]:.2f}"
            for i in range(len(historico["C1"]))
        )
        messagebox.showinfo("Histórico de Cálculos", historico_texto)
    else:
        messagebox.showinfo("Histórico de Cálculos", "Nenhum cálculo armazenado.")

historico = {
    "C1": [],
    "V1": [],
    "C2": [],
    "V2": []
}

root = tk.Tk()
root.title("Cálculo - C1 x V1 = C2 x V2")

tk.Label(root, text="C1:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_c1 = tk.Entry(root)
entry_c1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="V1:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_v1 = tk.Entry(root)
entry_v1.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="C2:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_c2 = tk.Entry(root)
entry_c2.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="V2:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_v2 = tk.Entry(root)
entry_v2.grid(row=3, column=1, padx=10, pady=5)

btn_calcular = tk.Button(root, text="Calcular", command=calcular)
btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

btn_historico = tk.Button(root, text="Mostrar Histórico", command=mostrar_historico)
btn_historico.grid(row=5, column=0, columnspan=2, pady=5)

btn_sair = tk.Button(root, text="Sair", command=root.quit)
btn_sair.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
