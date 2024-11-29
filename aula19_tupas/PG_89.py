import os
os.system("cls")

lista = [1,2,3,4,5,6,7,8,9]
print(lista)

lista2 = lista
tupa1 = tuple(lista)
print(lista2)

numero = input("digite um numero.: ")
lista.append(numero)
print(f"1 - {lista}")
print(f"2 - {lista2}")
print(f"t - {tupa1}")