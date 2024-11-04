#Faça um programa que receba um valor e mostre sua raiz quadrada. Para raízes que não são exatas, \
# arredonde para cima ou para baixo. Faça a validação para números negativos, \
# avisando ao usuário que o resultado será um número complexo.

import os
import math
import random

os.system("cls")

numero = 0
raiz = 0

numero = float(input("digite um numero.:  "))
if (numero < 0):
    print("=" *20)    
    print("Atenção: numero negativo, o resultado será um numero complexo")

absoluto = abs(numero)

raiz = math.sqrt(absoluto)

arredondado = round(raiz)
print("=" *20)
print(f"A raiz arredondada de.: {numero: .2f} é .: {raiz: .2f}, sendo seu valor arrdondado .: {arredondado: .2f}")
print("=" * 20)