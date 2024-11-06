# Faça um programa que receba o nome completo de uma pessoa e,\
# em seguida, mostre o primeiro e o último nome.



import os
os.system("Cls")

#declarando variaveis
nome = ""
primeiro_nome = ""
ultimo_nome = ""
lista_nome = ""
quantidade_nome = 0

#atribuindo variaveis
nome = input("digite o seu nome completo.: ")

lista_nome = nome.split(" ")
quantidade_nome = int(len(lista_nome))
primeiro_nome = lista_nome[0]
ultimo_nome = lista_nome[quantidade_nome-1]
#teste
#print (nome)
#print (lista_nome)
#print (quantidade_nome)
#print (primeiro_nome)
#print (ultimo_nome)
#saida dos dados
print("=" *20)
print(f"O nome completo é.: {nome} , o primeiro nome é.: {primeiro_nome} e o ulimo nome é.: {ultimo_nome}")
print("=" *20 )
