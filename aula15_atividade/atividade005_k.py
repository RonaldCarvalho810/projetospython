#Crie um programa que pede que o usuário digite um nome ou uma frase, 
#verifique se esse conteúdo digitado é um palíndromo ou não, 
#exibindo em tela esse resultado
import os

os.system("cls")

base = input("digite uma palavra ou frase..: ").replace(" ","").lower()

invertida = base[::-1]

print(f"..: {base} > {invertida}")

if(base == invertida):
    print("é palíndromo")
else:
    print("nao é palíndromo")