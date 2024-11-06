# Faça um programa que receba um número inteiro e mostre na tela:\
# A quantidade de unidades, a quantidade de dezenas, a quantidade de centenas e a quantidade de milhares.


import os
os.system("Cls")

#declarando variaveis
numero = 0
quantidade_numeros = 0
unidade = 0
dezena = 0
centena = 0
milhar = 0

#atribuindo variaveis
numero = str(input("digite um numero inteiro, entre 1 e 9999.: "))

if(int(len(numero))>4):
    print("numero fora da range de calculo")

#conferindo quantos numeros tem
quantidade_numeros = len(numero)

if(quantidade_numeros == 1):
    unidade = numero[0]
    dezena = 0
    centena = 0
    milhar = 0
elif(quantidade_numeros == 2):
    unidade = numero[1]
    dezena = numero[0]
    centena = 0
    milhar = 0
elif(quantidade_numeros == 3):
    unidade = numero[2]
    dezena = numero[1]
    centena = numero[0]
    milhar = 0
elif(quantidade_numeros == 4 ):
    unidade = numero[3]
    dezena = numero[2]
    centena = numero[1]
    milhar = numero[0]

#saida dos dados
print("=" *20)

print (f"o numero possui.: {unidade} unidades, {dezena} dezenas, {centena} centenas, {milhar} milhares ")
#print (f" o nome possui..: {tamanho_nome} palavras")
print("=" *20)