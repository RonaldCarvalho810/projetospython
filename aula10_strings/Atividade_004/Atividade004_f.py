# Faça um programa que receba o nome completo de uma pessoa e, posteriormente, imprima esse nome separadamente.


import os
os.system("Cls")

#declarando variaveis
nome = ("")
Nome_partido = ("")
tamanho_nome = 0

#atribuindo variaveis
nome = str(input("digite seu nome completo.: "))

#partindo o nome em partes

Nome_partido = nome.split(" ")

tamanho_nome = len(Nome_partido)

#print (Nome_partido)
#print (tamanho_nome)

#saida dos dados

print (f"o nome separado ficara assim..: {Nome_partido}")
print (f" o nome possui..: {tamanho_nome} palavras")
print("=" *20)