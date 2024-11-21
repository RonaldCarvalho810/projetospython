import os
os.system("cls")
# minha_lista = [1, 2, 3]
# minha_lista.append(4)
# print(minha_lista)

insercoes = int(input("digite o quantos numeros deverao ser inseridos.: "))
lista = []

for principal in range(0,insercoes):
    numeros = input("digie um numero.: ")
    lista.append(numeros)
print(lista)

busca = input("digite um numero para busca.: ")
if (busca in lista):
    print("encontrado")
    quantidade = lista.count(busca)
    print(f"foram localizados {quantidade} registros")
else:
    print("não encontrado")