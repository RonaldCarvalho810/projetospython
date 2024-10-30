#A empresa "SalaryBoost" está implementando um sistema automatizado para calcular os aumentos salariais de seus funcionários com base em critérios específicos. 
# Eles precisam de um programa que receba como entrada o salário atual de um funcionário e, em seguida, calcule o novo salário com base em determinadas condições. 
# Essas condições incluem um aumento de 5% caso o salário atual seja superior a R$1500,00, e um aumento de 10% caso o salário atual seja inferior a R$1000,00. 
# Além disso, o programa deve garantir que o salário informado não seja igual a zero ou negativo, pois isso não seria válido.

import os


os.system("cls")

print("=" * 20)
print("modulo para calculo de salarios..:")
print("=" * 20)

#definindo valores das mariaveis
salario_base = 0
salario_final = 0


salario_base = float(input("digite o valor do salario base..:"))

if (salario_base<=0):
    salario_base = float(input("valor de salario nao pode ser igual ou infeior a zero, favor inserir novamente..:"))

#calculando parametros
if (salario_base > 1500):
    salario_final = salario_base * 1.05
elif ( salario_base < 1000):
    salario_final = salario_base * 1.1
else:
    salario_final = salario_base

print("=" * 20)
print("resultado do calculo")
print(f"o salario do funcionario passou de..: {salario_base: .2f} para..: {salario_final: .2f}")
print("=" * 20)
print()
