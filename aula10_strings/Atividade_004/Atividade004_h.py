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

#atribuindo variaveis
nome = input("digite o nome.: ")

letras_nome = len(nome)
quantidade_o = nome.count("o")
lista_letras = list(nome)
posicao_primeiro_o = nome.find("o") +1
invertida = nome[::-1]
posicao_ultimo_o = invertida.find("o") + letras_nome


#teste
#print (nome)
#print (letras_nome)
#print (quantidade_o)
#print (lista_letras)
#print (posicao_primeiro_o)
#print (posicao_ultimo_o)

#saida dos dados
print("=" *20)
print(f"O nome.: {nome} , possui {quantidade_o} o, o primeiro na posicao.: {posicao_primeiro_o} e o ultimo na posicao.: {posicao_ultimo_o}")
print("=" *20 )
