import os
os.system("cls")

print("=" *30)
print("estrutura de controle for range")
print("=" *30)

print()

# primeira forma de montar a estrutura
# end= coloca os numeros em linha
for var_iteradora in range(1,7):
    print(f"valor: {var_iteradora}", end=" | ")
print()
print()

#segunda forma de montar a estrutura

inicio = 1
fim = 7
passo = 2

for var_iteradora in range(inicio,fim,passo):
    print(f"valor: {var_iteradora}" , end=" | ")
print()
print()