#Crie um programa que pergunte o ano de nascimento do usuário e calcule sua idade atual.

import os

os.system("cls")
import datetime

from datetime import datetime

data_nascimento_str = input("Digite sua data de nascimento (dd/mm/aaaa): ")

data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")

data_atual = datetime.now()

idade = data_atual.year - data_nascimento.year

if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
    idade -= 1

print(f"Sua idade é: {idade} anos")
