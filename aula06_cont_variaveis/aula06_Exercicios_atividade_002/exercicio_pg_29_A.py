import os


os.system("cls")

print("=" * 20)
print("modulo para conferir a existencia de um triangulo..:")
print("=" * 20)

#atribuindo valores das mariaveis
lado1 = 0
lado2 = 0
lado3 = 0
status =""

lado1 =float(input("digite o 1º lado..:"))
lado2 =float(input("digite o 2º lado..:"))
lado3 =float(input("digite o 3º lado..:"))

#checando requisitos do triangulo

if(lado1 + lado2 > lado3 and lado2 + lado3 > lado1 and lado1 + lado3 > lado2):
    status = "os lados formam um triangulo"
else:
    status = "os lados não formam um triangulo"

print("=" * 20)
print("resultados")
print("=" * 20)
print(f"as medidas..: {lado1} x {lado2} x {lado3} ..: {status}")
print("=" * 20)
print()
