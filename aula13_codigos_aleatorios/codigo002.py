#Faça um programa que leia uma frase e depois exiba na tela:
# A frase em minúsculas, a frase em maiúsculas, a quantidade de caracteres na frase e quantas letras tem a 2ª palavra na frase.

import os

os.system("cls")

frase = input("digite uma frase..: ")

teste_renato = frase.replace(" ","")

teste2_renato = frase.strip("e")

print(teste_renato)


#exit()
maiusculo = frase.upper()
minusculo = frase.lower()

quantidade = len(frase)
lista = frase.split(" ")

segunda_palavra = len(lista[1])
print(lista)
#exit()
print(f" A frase em maiusculo: {maiusculo}")
print(f" A frase em minusculo..: {minusculo}")
print(f" A frase tem ..: {quantidade} caracteres")
print(f" A segunda palavra tem..: {segunda_palavra} caracteres")