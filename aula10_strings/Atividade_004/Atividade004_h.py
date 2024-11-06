# Faça um programa que leia o nome de um aluno e mostre quantas vezes a letra 'o' aparece e\
# em que posição ela aparece pela primeira e última vez.



import os
os.system("Cls")

#declarando variaveis

nome = ""
quantidade_o = 0
posicao_primeiro_o = 0
posicao_ultimo_o = 0

#atribuindo variaveis
nome = input("digite o nome.: ")

quantidade_o = len(nome)
posicao_primeiro_o = nome.find("o") +1
posicao_ultimo_o = nome.rfind("o") +1

#saida dos dados
print("=" *20)
print(f"O nome.: {nome} , possui {quantidade_o} letra o, o primeiro na posicao.: {posicao_primeiro_o} e o ultimo na posicao.: {posicao_ultimo_o}")
print("=" *20 )
