#Desenvolva um programa que solicite um valor em reais e calcule quantos dólares podem ser comprados com esse valor.


import os

os.system("cls")

reais = float(input("digite o valor em reais..: "))
cotacao = float(input("digite a cotacao do dolar"))

resultado = reais / cotacao

print(f"Conversão direta, {reais } reais = {resultado} dolares")
print()
