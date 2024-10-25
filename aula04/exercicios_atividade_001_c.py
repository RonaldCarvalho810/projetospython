#Elabore um programa que receba quatro notas de um aluno e calcule a média dessas notas.

import os

os.system("cls")

nota1 = float(input("digite a nota 1..:"))
nota2 = float(input("digite a nota 2..:"))
nota3 = float(input("digite a nota 3..:"))
nota4 = float(input("digite a nota 4..:"))

media = (nota1 + nota2 + nota3 + nota4) / 4

print(f"a média das notas é..: {media}")
