import os


os.system("cls")

print("=" * 20)
print("insira 3 numeros..:")
print("=" * 20)

#definindo valores das mariaveis
maior = 0
menor = 0
iguais = "não são iguais"

numero1 =int(input("digite o 1º numero..:"))
numero2 =int(input("digite o 2º numero..:"))
numero3 =int(input("digite o 3º numero..:"))

#conferindo igualdae entre numeros
if (numero1 == numero2 and numero1 == numero3):
    iguais = "os tres numeros são iguais"
else:
    iguais = "os tres numeros são diferentes"

#conferindo quais dos numeros sao o maior e o menor

if (numero1 > numero2 and numero1 > numero3):
    maior = numero1
elif (numero2 > numero1 and numero2 > numero3):
    maior = numero2
else:
    maior = numero3

if (numero1 < numero2 and numero1 < numero3):
    menor = numero1
elif (numero2 < numero1 and numero2 < numero3):
    menor = numero2
else:
    menor = numero3

print("=" * 20)
print("resultados")
print(iguais)
print(f"o maior numero é o..: {maior} e o menor é o..: {menor}")
print("=" * 20)
print()
