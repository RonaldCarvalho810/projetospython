import os

os.system("cls")

base = input("digite uma palavra ou frase..: ").replace(" ","").lower()

invertida = base[::-1]

print(f"..: {base} > {invertida}")

if(base == invertida):
    print("é palíndromo")
else:
    print("nao é palíndromo")