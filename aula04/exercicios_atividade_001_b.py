#Crie um programa que pergunte o ano de nascimento do usuário e calcule sua idade atual.

import os

os.system("cls")
import datetime

from datetime import datetime

# Solicita a data de nascimento do usuário no formato dd/mm/aaaa
data_nascimento_str = input("Digite sua data de nascimento (dd/mm/aaaa): ")

# Converte a data de nascimento para um objeto datetime
data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")

# Obtém a data atual
data_atual = datetime.now()

# Calcula a idade
idade = data_atual.year - data_nascimento.year

# Ajusta se o aniversário ainda não ocorreu este ano
if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
    idade -= 1

print(f"Sua idade é: {idade} anos")
