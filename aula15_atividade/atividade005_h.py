#Faça um programa que imprima os valores no intervalo definidos pelo usuário.
#  Defina 3 números que deverão ser ignorados, ou seja, 
#que não serão impressos na tela
import os
os.system("cls")


inicio = int(input("digite o numero inicial.: "))
final = int(input("digite o numero final.: "))
ignorar = input("digite 3 numeros para serem ignorados (exemplo: 5-7-9).: ")
for var_a in range (inicio, final+1):
    if (str(var_a) in ignorar):
        continue
    else:
        print(f"{var_a}", end="|")
