import os
os.system("cls")

print("=" *30)
print("teste estrutura while")
print("=" *30)

print()

contador = 1

while (contador < 7):
    contador += 1
    if contador== 4:
        print(f"contador chegou em.: {contador}. break no while")
        break
else:
    print("while finalizado")