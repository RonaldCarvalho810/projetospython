#Evolua o programa anterior para um código que 
#pergunte ao usuário qual o intervalo que ele deseja ver  impresso
import os
os.system("cls")

inicio = int(input("digite o primeiro numero.: "))
final = int(input("digite o ultimo numero.: ")) +1

for var_a in range (inicio,final):
    print(f"index = {var_a}", end= "|")