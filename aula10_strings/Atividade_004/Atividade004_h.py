# Faça um programa que leia o nome de um aluno e mostre quantas vezes a letra 'o' aparece e\
# em que posição ela aparece pela primeira e última vez.



import os
os.system("Cls")

#declarando variaveis
nome = ""
quantidade_o = 0
letras_nome = 0
posicao_primeiro_o = 0
posicao_ultimo_o = 0
lista_letras = ""
string_resto = ""
posicao_ultimo_o_quebra = 0
posicao_ultimo_o_quebra_final = 0

#atribuindo variaveis
nome = input("digite o nome.: ")

#utilizando string invertida
letras_nome = len(nome)
quantidade_o = nome.count("o")
#lista_letras = list(nome)
posicao_primeiro_o = nome.find("o") +1
invertida = nome[::-1]
posicao_ultimo_o = invertida.find("o") + letras_nome

#utilizando quebra de string
string_resto = nome[posicao_primeiro_o : letras_nome]
posicao_ultimo_o_quebra = string_resto.find("o") +1
posicao_ultimo_o_quebra_final = posicao_primeiro_o + posicao_ultimo_o_quebra

#-----------------------------------
#testando saidas
#print(string_resto)
#print(posicao_ultimo_o_quebra_final)
#-----------------------------------

#-----------------------------------
#teste
#print (nome)
#print (letras_nome)
#print (quantidade_o)
#print (lista_letras)
#print (posicao_primeiro_o)
#print (posicao_ultimo_o)
#-----------------------------------

#saida dos dados
print("=" *20)
print("utilizando inversao de string")
print(f"O nome.: {nome} , possui {quantidade_o} o, o primeiro na posicao.: {posicao_primeiro_o} e o ultimo na posicao.: {posicao_ultimo_o}")
print("=" *20 )
print("utilizando quebra de string")
print(f"O nome.: {nome} , possui {quantidade_o} o, o primeiro na posicao.: {posicao_primeiro_o} e o ultimo na posicao.: {posicao_ultimo_o_quebra_final}")
print("=" *20 )
