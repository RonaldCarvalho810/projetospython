import os
os.system("cls")

lista_inteira = []
lista1 = [1,2,3,4,5]
lista2 = [6,7,8,9,10]

lista_inteira.extend(lista1)

#lista_inteira.append(lista2)

#print(lista_inteira)

lista_inteira.extend(lista2)

print(lista_inteira)

soma = sum(lista_inteira)

print(soma)