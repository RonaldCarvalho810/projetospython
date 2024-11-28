import os
os.system("cls")

lista = []
lista_base = []

principal = input("digite um mumero.: ")
while (principal != "s"):
    lista.append(float(principal))
    principal = input("digite um numero.: ")

lista_base= lista

print(f"lista base{lista_base}")
lista.sort()
print(f" lista ordenada {lista}")
lista.reverse()
print(f" lista inversa {lista}")
maior = max(lista)
menor = min(lista)
soma = sum(lista)
itens = len(lista)
media = soma / itens
print(f"a LISTA possui.: {itens} itens")
print(maior)
print(menor)
print(f" a media é.: {media: .2f}")
print(f"a soma é.: {soma: .2f}")

remover = float(input("digite um valor para remover.:"))

while (lista.count(remover)>0):
    lista.remove(remover)

lista.sort()
print(lista)