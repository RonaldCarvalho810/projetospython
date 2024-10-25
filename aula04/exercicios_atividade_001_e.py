#Faça um programa que receba um número inteiro e exiba seu sucessor e antecessor.

import os

os.system("cls")

num1 = int(input("digite o 1ª numero..: "))

anterior = num1 - 1
posterior = num1 + 1


print (f"o numero {num1} é antecedido por : {anterior} e sucedido por : {posterior}.")
