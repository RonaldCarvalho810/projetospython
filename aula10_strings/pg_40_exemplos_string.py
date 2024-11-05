import os
os.system("cls")

print("=" *20)
print("fatiamento de string")
print("=" *20)

frase = "string em python"

print(f"string original.: {frase}")

primeiros_cinco = frase[:5]
print(f"primeiros cinco caracteres.: {primeiros_cinco}")

ultimos_dez = frase[-10:]
print(f"ultimos dez..: {ultimos_dez}")

quarto_ao_decimos = frase[3:10]
print(f"do quarto ao decimo..: {quarto_ao_decimos}")

a_cada_dois = frase[::2]
print(f"a cada dois caracteres..: {a_cada_dois}")

invertida = frase[::-1]
print(f"invertida..: {invertida}")
print("=" *20)