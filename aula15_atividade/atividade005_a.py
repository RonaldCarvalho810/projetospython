#Faça um programa que imprima os números no intervalo entre 1 e 100. 
#Os números devem ser apresentados na horizontal.
import os
os.system("cls")

for var_a in range (1,101):
    print(f"index = {var_a}", end= "|")