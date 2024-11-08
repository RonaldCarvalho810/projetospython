import os
os.system("cls")
import random

from rich import  print

numeros = [10, 20, 30, 40, 50, 60, 70, 80, 90,100]


#numero = random.choice(numeros)

print("AS CARTAS ESTÃO NA MESA")
print(numeros)
random.shuffle(numeros)
#print(numeros)
print("AS CARTAS ESTÃO SENDO EMBALHARADAS, AGUARDE...")

jogador1 = int(input("jogador 1, por favor, escolha uma carta entre 1 e 10..: "))
jogador1_carta = numeros[jogador1]
print(f" o jogador 1 escolheu a carta..: {jogador1_carta}")
jogador2 = int(input("jogador 1, por favor, escolha uma carta entre 1 e 10..: "))
jogador2_carta = numeros[jogador2]
print(f" o jogador 1 escolheu a carta..: {jogador2_carta}")

if( jogador1_carta> jogador2_carta):
    print("[red]Jogador 1 venceu[/RED]")
else:
    print("[green]Jogador 1 venceu[/green]")