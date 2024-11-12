import os
os.system("cls")

print("=" *30)
print("estrutura de controle somatório")
print("=" *30)

print()

soma = 0

for var_iteradora in range(0,4):
    numero = int(input(f"digite o {var_iteradora}º numerop..:"))
    soma +=numero

print("=" *30)
print(f"soma de numeros é..: {soma}")
print("=" *30)