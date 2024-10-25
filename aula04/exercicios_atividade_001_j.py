#Elabore um programa que peça as dimensões de um retângulo e calcule seu perímetro.

#importando blibioteca
import os

#limpando terminal
os.system("cls")

#recebendo os valores dos lados do triangulo
lado1 = int(input("digite o 1º numero..:"))
lado2 = int(input("digite o 2º numero..:"))
lado3 = int(input("digite o 3º numero..:"))

#calculando o perimetro
perimetro = lado1 + lado2 + lado3

#mostrando o perimetro no terminal - Saída
print(f" O perímetro de um triangulo com os lados..: {lado1} x {lado2} x {lado3} é..: {perimetro}")
print()
