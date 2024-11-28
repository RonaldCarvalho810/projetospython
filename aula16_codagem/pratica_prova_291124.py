import os
os.system("cls")
lista = []
pares = []
impares =[]
lista_original=[]
busca = 0
for a in range(0,52):
    lista.append(int(a))
    if (a%2 == 0):
        pares.append(a)
    else:
        impares.append(a)
#print(lista)
maior = max(lista)
menor = min(lista)
tamanho = len(lista)
soma = sum(lista)


lista_original = lista.copy()
print(lista_original)
print(lista)
lista.reverse()
print(lista)
print(f"os pares sao: {pares}")
print(f"os impares sao: {impares}")
print(f"a lista tem {tamanho} itens, seu \
maior valor é: {maior} e seu menor valor é: {menor} \
a soma dos valores é: {soma}")
busca = int(input("digite um numero para busca>: "))
if (busca in lista_original):
    indice = lista_original.index(busca)
print(indice)
