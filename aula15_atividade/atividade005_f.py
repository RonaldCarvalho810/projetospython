#Faça um programa que imprima os números primos entre 0 e 100
import os
os.system("cls")


for principal in range(2, 101):
    divisores = 0
    for var_a in range(1, principal + 1):
        if principal % var_a == 0:
            divisores += 1
    if (divisores== 2):

        print(f"O número {principal} é um numero primo.")
