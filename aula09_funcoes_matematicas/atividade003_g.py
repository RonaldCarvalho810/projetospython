#Faça um programa que peça os valores de a, b e c de uma equação do 2º grau.\
#  Calcule as raízes da equação do\
#  2º grau seguindo a fórmula: Δ = b² - 4ac, x = (-b ± raiz(Δ)) / (2a)

import os
import math
import random

os.system("cls")

print("=" * 20)
print("modulo para calcular uma equação de segundo grau ")
print("=" * 20)
print("regra para calculo das raizes.: ax² + bx + c =0 ")
#atribuindo valores das mariaveis

a = int(input("digite o valor de a.: "))
b = int(input("digite o valor de b.: "))
c = int(input("digite o valor de c.: "))
delta = 0
primeira_raiz = 0
segunda_raiz = 0

#calculando o delta
delta = (math.pow(b,2)) - (4*a*c)

primeira_raiz = (-(b) + (math.sqrt(delta) )) / 2*a
segunda_raiz = (-(b) - (math.sqrt(delta) )) / 2*a

print("=" * 20)

print("=" * 20)
print(f"as raizes da equação..: (x²-6x+5=0) são  x¹={primeira_raiz} e x²={segunda_raiz} ")
print("=" * 20)
print()