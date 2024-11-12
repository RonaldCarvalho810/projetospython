import os
import random
from rich import print
os.system("cls")

print("=" *30)
print("teste estrutura for")
print("=" *30)

print()

lista = list()

limite = int(input("digite o numero limite.: "))
#lista = []
for contador in range (0, limite ):
    nome = input("digite um nome.: ")
    lista.insert(0,nome)
print(lista)

sorteado = random.choice(lista)

print(f"o sorteado foi>:[red] {sorteado}[/red]")