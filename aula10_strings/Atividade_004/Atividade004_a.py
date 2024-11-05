#Faça um programa que solicite separadamente o nome, o nome do meio e o sobrenome de uma pessoa. Em seguida, imprima o nome completo.
import os
os.system("Cls")

#declarando variaveis
primeiro_nome = ("")
Nome_do_meio = ("")
Sobrenome =("")

#atribuindo variaveis

primeiro_nome = str(input("Digite o primeiro nome.: "))
Nome_do_meio = str(input("Digite o nome do meio.: "))
Sobrenome = str(input("Digite o Sobrenome.: "))

nome_completo = primeiro_nome + " " + Nome_do_meio + " " + Sobrenome

print("="*20)
print(f"o nome completo é.: {nome_completo}")
print("=" *20)
