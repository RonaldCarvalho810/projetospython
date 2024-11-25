#Faça um programa que leia um número indeterminado de notas (pressione ‘s’ ou ‘0’ para sair).

# Após esta entrada de dados, faça o seguinte:
# • Mostre a quantidade de notas que foram lidas.
# • Exiba todas as notas na ordem em que foram informadas.
# • Exiba todas as notas na ordem inversa à que foram informadas, uma abaixo da outra.
# • Calcule e mostre a soma das notas.
# • Calcule e mostre a média das notas.

import os
os.system("cls")

notas = []
quantidade = 0
inversa = []
soma = 0
media = 0
inserir = input("digite uma nota.: ")
#notas.append(inserir)
while inserir != "0" and inserir != "s":
    notas.append(inserir)
    soma += int(inserir)
    inserir = input("digite uma nota.: ")

print("iniciando estatisticas...")

quantidade = len(notas)
inversa = notas[::-1]
media = (soma / quantidade)
print("=" * 50)
print("saidas")
print(f"A lista tem {quantidade} notas")
print(f" lista na ordem de insercao : {notas}")
print(f" lista na ordem inversa : ")
for principal in range(0, quantidade):
    print(inversa[principal])
print(f"a soma das notas foi..: {soma}")
print(f"a media geral foi.: {media}")
print("=" * 50)