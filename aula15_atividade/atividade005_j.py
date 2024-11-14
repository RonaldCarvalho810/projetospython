#Crie um programa que realiza a contagem de 1 até 100, usando apenas de números ímpares, 
#ao final do processo exiba na tela quantos números ímpares foram encontrados nesse intervalo, 
#assim como a soma dos mesmos
import os
os.system("cls")

contador = 0
soma = 0

for externa in range(1,101,2):
    contador +=1
    soma += externa
    print(f"{externa}", end="|")

print(f"essa faixa numerica, tem {contador} numeros impares e seu total é.: {soma}")