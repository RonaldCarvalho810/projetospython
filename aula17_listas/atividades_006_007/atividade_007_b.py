import os
os.system("cls")
import random


lista = []
numero = 0

for principal in range(0,15):
    numero = random.randint(0,50)
    lista.append(numero)
lista.sort()

print(lista)
print(lista[0:5])
print(lista[5:10])
print(lista[10:15])
#print(lista)
