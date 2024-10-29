#Implemente um programa que receba dois números e realize a divisão, formatando o resultado com quatro casas decimais.

import os

os.system("cls")

num1 = int(input("digite o 1ª numero..: "))
num2 = int(input("digite o 2ª numero..: "))

resultado = num1 / num2
formatado = f"{resultado:.4f}"

print (formatado)