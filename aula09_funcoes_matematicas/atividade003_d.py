#Faça um programa que receba um ângulo qualquer. Em seguida, calcule o seno, cosseno e tangente do ângulo, limitando a saída a 2 casas decimais.

import os
import math
import random

os.system("cls")

angulo = 0
seno = 0
coseno = 0
tangente = 0

angulo = float(input("digite a baseo..: "))


seno = math.sin(math.radians(angulo)) 
coseno = math.cos(math.radians(angulo))
tangente = math.tan(math.radians(angulo))

print("=" *20)
print(f"o angulo.: {angulo: .2f} posui.: ")
print(f"seno .: {seno: .2f}, coseno .: {coseno: .2f} e tangente.: {tangente: .2f}"   )
print("=" * 20)