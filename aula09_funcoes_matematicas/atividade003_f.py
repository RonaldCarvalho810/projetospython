#Faça um programa onde o usuário tenta adivinhar o número que o computador está ‘pensando’.

import os
import math
import random

os.system("cls")

numero = random.randint(1,20)
numero_usuario = int(input("digite um numero entre 1 e 50..: "))

print("=" *20)
print(f"o computador selecionou..: {numero: .2f} e você..: {numero_usuario} ")
print("=" * 20)

if(numero_usuario>numero):
    print("parabens, vc ganhou")
elif(numero>numero_usuario):
    print("infelizmente você perdeu")
else:
    print("deu empate")