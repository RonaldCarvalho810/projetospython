# Faça um programa que receba uma frase e, em seguida, mostre quantas vezes as vogais foram utilizadas.


import os
os.system("Cls")

#declarando variaveis
frase = ("")

quantidade_caracteres_a = 0
quantidade_caracteres_e = 0
quantidade_caracteres_i = 0
quantidade_caracteres_o = 0
quantidade_caracteres_u = 0

#atribuindo variaveis
frase = str(input("digite uma frase.: "))

#contagem das vogais
quantidade_caracteres_a = frase.count("a")
quantidade_caracteres_e = frase.count("e")
quantidade_caracteres_i = frase.count("i")
quantidade_caracteres_o = frase.count("o")
quantidade_caracteres_u = frase.count("u")

#saida dos dados
print(f"a frase.: {frase}") 
print(f"a frase possui : {quantidade_caracteres_a} letras a")
print(f"a frase possui : {quantidade_caracteres_e} letras e")
print(f"a frase possui : {quantidade_caracteres_i} letras i")
print(f"a frase possui : {quantidade_caracteres_o} letras o")
print(f"a frase possui : {quantidade_caracteres_u} letras u")
print("=" *20)