import os


os.system("cls")

a = 10
b = 5
c = "john"

print("=" * 50)
print("condicionais operadores logicos")
print("=" * 50)

print(" E (and) verdadeiro")
if (a >5 and b != c):
    print(" verdadeiro: bloco executado")
else:
    print("falso: bloco executado")

print("=" * 50)

print(" E (and) falso")
if (a >5 and b == c):
    print(" verdadeiro: bloco executado")
else:
    print("falso: bloco executado")

print("=" * 50)

print(" or (ou) verdadeiro")
if (a >5 or b == c):
    print(" verdadeiro: bloco executado")
else:
    print("falso: bloco executado")

print("=" * 50)

print(" E (and) falso")
if (a < 5 or b == c):
    print(" verdadeiro: bloco executado")
else:
    print("falso: bloco executado")

print("=" * 50)
print()