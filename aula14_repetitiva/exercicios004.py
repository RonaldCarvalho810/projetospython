import os
os.system("cls")

print("=" *30)
print("estrutura de controle com validacao e casting")
print("=" *30)

print()

soma = 0

for c in range(0,5):
    
    numero = input("digite um numero de (0 - 5)")
    if (not (numero.isnumeric())):
        print("entrada invalida")
        print()
    else:
        numero = int(numero)

        if (numero>=0 and numero<=5):
            print("o numero esta dentro do intervalo")

        else:
            print("entrada invalida")
            print()

print("=" *30)

print("=" *30)
print()