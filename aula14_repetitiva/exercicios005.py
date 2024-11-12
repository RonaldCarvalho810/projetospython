import os
os.system("cls")

print("=" *30)
print("estrutura de controle com validacao e casting")
print("=" *30)

print()

for c in range(1,11):
    if( c== 5):
        print(f"o numero {c} esta fora do loop")
        continue
    print(f"o numero é.: {c}")

print("=" *30)
print()

exit() # continuar teste depois
limite = int(input("digite o numero limite"))
#lista = []
for contador in range (0, limite ):
    lista = input("digite um nome")

print(lista)
