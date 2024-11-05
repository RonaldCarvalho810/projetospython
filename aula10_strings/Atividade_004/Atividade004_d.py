#Faça um programa que leia uma frase e depois exiba na tela:\
#  A frase em minúsculas, a frase em maiúsculas, a quantidade de caracteres na frase e quantas letras tem a 2ª palavra na frase.

import os
os.system("Cls")

#declarando variaveis
frase = ("")
frase_maiusculo =("")
frase_minusculo =("")
quantidade_caracteres = 0

#atribuindo variaveis
frase = str(input("digite uma frase.: "))

frase_maiusculo = frase.upper()
frase_minusculo = frase.lower()
quantidade_caracteres = len(frase)

#posicao = frase.find(" ")

Variavel_lista = frase.split(" ")

print(Variavel_lista)
#print(f"posicao = {posicao}")
segunda_palavra = len(Variavel_lista(1))

print(f"a frase.: {frase}") 
print(f"a frase em maiusculo.: {frase_maiusculo}")
print(f"a frase em minusculo.: {frase_minusculo}")
print(f"a frase tem : {quantidade_caracteres} caracteres")
print(f"a segunda palavra tem : {segunda_palavra} caracteres")
print("=" *20)