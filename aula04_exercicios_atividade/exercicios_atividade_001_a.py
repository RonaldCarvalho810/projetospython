#a - Desenvolva um programa que solicite três valores ao usuário. Em seguida, calcule e exiba a soma e a multiplicação desses valores.
import os

os.system("cls")

num1 = int(input("digite o 1ª numero..:"))
num2 = int(input("digite o 2ª numero..:"))
num3 = int(input("digite o terceiro numero..:"))

soma = num1 + num2 + num3
produto = num1 * num2 * num3

print(f"o valor da soma oos valores é {soma} ")
print(f"o produto dos valores é: {produto}")