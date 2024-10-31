import os 
import datetime

os.system("cls")

from datetime import datetime

data_inicio_str = input("Digite a data de início (dd/mm/aaaa): ")

data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")

data_fim = datetime.now()

diferenca = data_fim - data_inicio
print(f"O período entre a data de início e hoje é de {diferenca.days} dias.")

#novo
#idade = diferenca/365.2
idade = diferenca.days / 365.2
print(f"sua idade é.: {idade:.2f}")
