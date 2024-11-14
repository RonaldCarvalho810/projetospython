#Faça um programa que calcule os números primos em um intervalo pré-determinado pelo usuário
import os
os.system("cls")


inicio = int(input("digite o numero inicial.: "))
final = int(input("digite o numero final.: "))
for principal in range(inicio, final):
    divisores = 0
    for interna in range(1, principal + 1):
        if principal % interna == 0:
            divisores += 1
    if (divisores== 2):

        print(f"O número {principal} é um numero primo.")
