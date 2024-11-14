#Faça um programa que some a quantidade de números pares encontrados no intervalo entre 0 e 100
import os
os.system("cls")

soma = 0

for var_a in range (0,101,2):
    soma += var_a
    #print(f"index = {var_a}" , end= "|")
print(f" total da soma dos numeros pares nessa faixa entre 0 e 100 é..: {soma}")