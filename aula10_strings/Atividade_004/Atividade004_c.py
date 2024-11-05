#Faça um programa que leia o nome de uma pessoa e verifique se a palavra 'Oliveira' está presente neste nome, mostrando True ou False.

import os
os.system("Cls")

#declarando variaveis
nome = ("")

#atribuindo variaveis

nome = str(input("digite o nome.: "))

if("Oliveira" in nome):
    print("Dado validado")
else:
    print("dado não validado")

print("=" *20)