# conferir se o cliente é maior ou menor
import os
import datetime

os.system("cls")

from datetime import datetime

data_nascimento_str = input("Digite sua data de nascimento (dd/mm/aaaa): ")

data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")

data_atual = datetime.now()

idade = data_atual.year - data_nascimento.year

if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
    idade -= 1

if idade >= 18 : status = "maior"

else : status = "menor"

print (f" o cliente é.:  {status}")