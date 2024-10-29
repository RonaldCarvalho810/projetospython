#Eles precisam de um programa que permita aos usuários inserir um ano e, em seguida, determine se esse ano é bissexto ou não, 
# de acordo com as regras estabelecidas pelo calendário gregoriano. Além disso, é necessário realizar a validação de entrada de dados para 
# garantir que o ano inserido pelo usuário seja um valor válido, ou seja, um número inteiro positivo.


import os


os.system("cls")

print("=" * 20)
print("modulo para calculo de anos bisextos..:")
print("=" * 20)

#definindo valores das mariaveis
ano = 0
status = " não é um ano bisexto"
#entrada de dados
ano = int(input("digite o ano para checagem (é necessario que seja um numero inteiro)..:"))

#calculando parametros
if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
    status = " é um ano bisexto"
print("=" * 20)
print("resultado do calculo")
print(f"O ano.: {ano}{status}")
print("=" * 20)
print()
