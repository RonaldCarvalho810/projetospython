import os
import random

os.system("cls")

numero = int(input("digite um numero..:"))
print("=" *35)
if(numero % 2 ==0):
    print("par")
else:
    print("IMPAR")
print("=" *35)

print("============================fim===================================")

numero2 = int(input("digite um numero..:"))
numero3= int(input("digite um numero..:"))

if(numero2>numero3 and numero2 !=10) or (numero2== 1 and numero3==2):
    print("condicional positiva")
else:
    print("condicao nao atendida")

print("============================fim===================================")

valor = float(input("digite o valor.: "))
porcentagem = float(input("digite a porcentagem.: "))

porcentagem_de_desconto = (100 - porcentagem) /100

valor_final = (valor * porcentagem_de_desconto)

print(f"o valor com desconto apçicado será de..: {valor_final: .2f}")

valor_acrescido = valor * (1 + (porcentagem / 100 ))

print(f"o valor com acrescimo apçicado será de..: {valor_acrescido: .2f}")
print()
print()
print()

print("============================fim===================================")

numero_relacional = float(input("digite o primeiro valor..: "))
numero_base = float(input("digite o segundo valor..: "))

relacao = (numero_relacional / numero_base) *100

print(f" o segundo numero é..: {relacao: .2f}% do primeiro numero" )

print("============================fim===================================")

aleatorio = random.randint(0,100)

print(f" o numero aleatorio gerado é..: {aleatorio}")

print("============================fim===================================")