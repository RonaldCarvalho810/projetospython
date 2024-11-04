#Faça um programa que receba 2 valores, faça a divisão entre eles.\
#  Se a divisão não for inteira, o programa deverá arredondar o resultado para cima e para baixo.\
#  Faça a validação para divisão por 0.

import os
import math
import random

os.system("cls")

dividendo = 0
divisor = 0

dividendo = float(input("digite o dividendo..: "))
divisor = float(input("digite o divisor..: "))

if (divisor == 0):
    print("=" *20)    
    print("Atenção: numero negativo!!!")
    divisor = float(input("digite o divisor (numero nao pode ser 0..: "))
    print("Atenção: numero negativo!!!")

quociente = dividendo/divisor

if (dividendo % divisor !=0):
    arredondado_baixo = math.floor(quociente)
    arredondado_cima = math.ceil(quociente)
    status = "quebrado"
else:
    status = "inteiro"

print("=" *20)
print(f"o quociente da divisao do numero.: {dividendo: .2f} pelo numero .: {divisor: .2f}, é .: {quociente: .2f}")
if(status == "quebrado"):
    print(f"quociente não é inteiro, seu arredondamento é..: para cima : {arredondado_cima} e para baixo :{arredondado_baixo}")
print
print("=" * 20)