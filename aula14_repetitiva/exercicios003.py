import os
os.system("cls")

print("=" *30)
print("estrutura de controle com input e if")
print("=" *30)

print()

soma = 0

for var_iteradora in range(0,4):
    numero = int(input(f"digite o {var_iteradora}º numerop..:"))
    if(numero %2 ==0 ):
        print(f"o numero.: {numero} é par")
    else:   
        print(f"o numero.: {numero} é impar")
print("=" *30)

print(f"soma de numeros é..: {soma}")
print("=" *30)
print()