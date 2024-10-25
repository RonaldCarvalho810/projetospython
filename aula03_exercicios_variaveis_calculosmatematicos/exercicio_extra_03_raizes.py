import os

os.system("cls")

numero = int(input("digite um numero inteiro, para encontrar a raiz quadrada..:"))
raiz = numero ** (1/2)

print("=" * 20)
print(f"a raiz quadrada de {numero} é :{raiz}")
print("=" * 20)

numero = int(input("digite um numero inteiro, para encontrar a raiz cubica..:"))
raiz_cubica = numero ** (1/3)

print("=" * 20)
print(f"a raiz cubica de {numero} é :{raiz_cubica}")
print("=" * 20)