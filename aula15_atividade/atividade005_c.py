#Faça um programa que imprima os números no intervalo entre 1 e 10 em ordem inversa
import os
os.system("cls")

inicio = 11

for var_a in range (1,11):
    inicio -=1
    print(f"index = {inicio}" , end= "|")