#1 Trabalho sobre a estrutura de dados SET 
#Senac Minas Gerais/Juiz de Fora
#Aluno: Ronald José Almeida de Carvalho
#Turma: 0392
#Ano: 2024

# Objetivo  - O cliente deseja fazer um investimento em marketing e montar uma politica de fidelizacao para os clientes
#para isso ele precisa analisar os 3 tipos de atendimentos que possui, sendo eles: presencial, mobile e web

# 1 - crie tres sets um pra cada tipo de atendimento
# 2 - simule um banco de dados de contenha o cpf dos clientes em cada set, o cpf precisa ter 11 caracteres e nao ter todos seus numeros iguais 
# 3 - analise quantos clientes da loja presencial nunca compraram em outro meio
# 4 - analise quantos clientes da presencial ja compraram no mobile
# 5 - analise quantos clientes da presencial ja compraram no web
import os
import random

os.system("cls")

set_presencial = set()
set_mobile = set()
set_web = set()


for principal in range(1, 51):
    cpf = ""  
    while len(cpf) < 11:  
        digito = random.randint(0, 9)
        cpf += str(digito)  
    set_presencial.add(cpf)  


for principal in range(1, 51):
    cpf = ""  
    while len(cpf) < 11:  
        digito = random.randint(0, 9)
        cpf += str(digito)  
    set_mobile.add(cpf)


for principal in range(1, 51):
    cpf = ""  
    while len(cpf) < 11:  
        digito = random.randint(0, 9)
        cpf += str(digito)  
    set_web.add(cpf)

lista_presencial = list(set_presencial)

for a1 in range(1,11):
    set_mobile.add(lista_presencial[random.randint(0,len(lista_presencial))])
    set_web.add(lista_presencial[random.randint(0,len(lista_presencial))])        

# print("CPFs gerados (presencial):")
# print(set_presencial)

# print("CPFs gerados (mobile):")
# print(set_mobile)

# print("CPFs gerados (web):")
# print(set_web)

set_saida = set_presencial.difference(set_mobile,set_web)
set_saida2 = set_presencial.intersection(set_mobile)
set_saida3 = set_presencial.intersection(set_web)

os.system("cls")
lista_saida = list(set_saida)
lista_saida2 = list(set_saida2)
lista_saida3 = list(set_saida3)

print(f"esses sao os {len(set_saida)} cpfs de presencial que nao coincidem com os outros sets")
for a in range(0, len(lista_saida)):
    print(f"{lista_saida[a]}", end=" ")
    print()

print(f"esses sao os {len(set_saida2)} cpfs de presencial que coincidem com o set mobile")
for a in range(0, len(lista_saida2)):
    print(f"{lista_saida2[a]}", end=" ")
    print()

print(f"esses sao os {len(set_saida3)} cpfs de presencial que coincidem com o set web")
for a in range(0, len(lista_saida3)):
    print(f"{lista_saida3[a]}", end=" ")
    print()

print("fim da analise")