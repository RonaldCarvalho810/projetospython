#Faça um programa que receba o nome 'João da Silva' e, em seguida, substitua 'Silva' por 'Oliveira'.
import os
os.system("Cls")

#declarando variaveis
nome = ("")

#atribuindo variaveis

nome = "João da Silva"

nome_alterado = nome.replace("Silva", "Oliveira")

print("="*20)
print(f"o nome original é.: {nome}")
print(f"o nome alterado é.: {nome_alterado}")
print("=" *20)
