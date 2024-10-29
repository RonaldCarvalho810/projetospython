#Elabore um programa que peça as dimensões de um retângulo e calcule seu perímetro.

#importando blibioteca / modulo
import os

#limpando terminal
os.system("cls")

#entrada dos parametros
print("Entre com os parametros..:")
medida = str(input("informe a unidade de medida do triangulo, tipo.: cm, m, km ..: "))
lado1 = int(input("digite o 1º lado..: "))
lado2 = int(input("digite o 2º lado..: "))
lado3 = int(input("digite o 3º lado..: "))

#calculando o perimetro
perimetro = lado1 + lado2 + lado3

#mostrando o perimetro no terminal - Saída
print(f" O perímetro de um triangulo com os lados..: {lado1} {medida} x {lado2} {medida} x {lado3} {medida} é..: {perimetro} {medida}")
print()
