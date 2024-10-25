# importa biblioteca
import os
import datetime

os.system('cls')

print ("-" *70)
print ("variaveis strings")
print ("-" *70)

# entrada de dados

nome = input("entre com um nome :")
peso = input("entre com o peso :")
altura  = input("entre com a altura :")

# entrada com casting - forçando tipagem
nascimento = int(input("ano de nascimento :"))
cep = str(input("digite o cep :"))
bairro =str(input("digite o bairro :"))
rua = str(input(" Digite a rua :"))
numero = int(input ("digite o mumero :"))

ano_atual = datetime.datetime.now().year
idade = int(ano_atual) - nascimento

print ("-" *70)
print ("SAIDA DE DADOS")
print ("-" *70)
print ("nome ........: ", nome)
print ("ano de nascmento ........: ", nascimento)
print ("peso ........: ", peso)
print ("altura ........: ", altura)
#saida interpolada
print(f"{nome}, você tem {idade} anos!")
print(f"cep ...........:{cep}")
print(f"bairro ...........:{bairro}")
print(f"rua ...........:{rua}")
print(f"numero ...........:{numero}")
print ("-" *70)
print ("")
print ("")
print ("Finalizado")