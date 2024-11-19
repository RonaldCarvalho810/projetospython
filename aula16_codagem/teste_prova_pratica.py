import os
os.system("cls")

inicio = 0
final = 0
Soma = 0
divisor = 0
soma_divisores = 0
inicio= int(input("digite o primeiro numero.: "))
final=int(input("digite o ultimo numero.: "))

for principal in range(inicio,final + 1):
    soma_divisores = 0
    for interno1 in range(1,principal-1):
        if principal%interno1 == 0:
            soma_divisores += interno1
    if soma_divisores == principal:
        print(f"{principal} é perfeito")