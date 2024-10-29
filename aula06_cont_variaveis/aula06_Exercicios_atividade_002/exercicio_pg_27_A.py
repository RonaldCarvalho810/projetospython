import os


os.system("cls")

print("=" * 20)
print("conferemcia de tipo numerico ")
print("=" * 20)

numero =float(input("digite um numero..:"))
resposta = ""
if numero % 2 == 0:
    resposta = f"o numero {numero} é par"
else :
    resposta = f"o numero {numero} é impar"

print("=" * 20)
print (f" o numero inserido é{resposta}")
print("=" * 20)
