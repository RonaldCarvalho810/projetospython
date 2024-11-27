import os
os.system("cls")

# lista1 = [1,2,3]
# lista2 = [3,4,6]

# lista_final = lista1 + lista2

# print(lista_final)

# sorteado = lista_final.pop(0)
# print(sorteado)

# lista_final.sort()
# print(lista_final)

# teste = lista_final[::2]
# print(teste)

impares = []
pares = []
numero = (input("digite um numero.: - s para sair "))
lista = []
while (numero != "s" and numero != "0"):
    
    lista.append(int(numero))
    if (int(numero) %2==0):
        pares.append(numero)
    else:
        impares.append(numero)
    numero = (input("digite um numero.: - s ou 0 para sair "))
lista.sort()
print(lista)
print(pares)
print(impares)