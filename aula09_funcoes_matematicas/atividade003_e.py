#Faça um programa para sortear um número de 1 a 20

import os
import math
import random

os.system("cls")

numero = random.randint(1,20)

print("=" *20)
print(f"o numero selecionado foi.: {numero: .2f} ")
print("=" * 20)