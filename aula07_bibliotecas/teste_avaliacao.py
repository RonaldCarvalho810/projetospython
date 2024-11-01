import os
os.system("cls")

numero = int(input("digite um numero..:"))
print("=" *35)
if(numero % 2 ==0):
    print("par")
else:
    print("IMPAR")
print("=" *35)

numero2 = int(input("digite um numero..:"))
numero3= int(input("digite um numero..:"))

if(numero2>numero3 and numero2 !=10):
    print("condicional positiva")
else:
    print("condicao nao atendida")

print("fim")

valor = float(input("digite o valor"))
desconto = float(input("digite o desconto"))

porcentagem_de_desconto = (100 - desconto) /100

valor_final = (valor * porcentagem_de_desconto)

print(f"o valor com desconto apçicado será de..: {valor_final}")

valor_acrecido = valor * (1 + (desconto / 100 ))

print(f"o valor com desconto apçicado será de..: {valor_acrecido}")