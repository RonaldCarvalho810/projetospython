#Faça um programa que verifique se o usuário e senha estão inseridos em um banco de dados (fake). 
#O usuário só terá acesso se digitar os dados corretos e, assim, sair do laço
import os
os.system("cls")

usuario = str(input("digite seu cpf.:  "))
senha = str(input("digite sua senha.: "))
teste = usuario[0:3]
print(teste)
if (senha != usuario[0:3]): 
    status = "incorreto"
else:
    status = "autorizado"
print(status)
while (status == "incorreto"):
    
    print("usuario ou senha incorretos")
    usuario = input("digite seu cpf.:  ")
    senha = input("digite sua senha.: ")
    if (senha != usuario[0:3]): 
        status = "incorreto"
    else:
        status = "autorizado"
        print("sistema conectado!!!")