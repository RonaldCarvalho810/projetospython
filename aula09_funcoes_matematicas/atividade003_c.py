#Faça um programa que receba as informações de base e expoente. Calcule a potência.

import os
import math
import random

os.system("cls")

base = 0
expoente = 0

base = float(input("digite a baseo..: "))
expoente = float(input("digite o expoente..: "))

potencia = math.pow(base,expoente)

print("=" *20)
print(f"a potencia do numero.: {base: .2f} elevado ao numero .: {expoente: .2f}, é .: {potencia: .2f}")
print
print("=" * 20)