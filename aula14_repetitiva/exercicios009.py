import os
os.system("cls")

print("=" *30)
print("teste estrutura while else continue")
print("=" *30)

print()

contador = 0 


while (contador<= 10):
    contador +=1

    if(contador % 2 == 0):
        continue
    print(f"contador : {contador}")
else:
        print(f"bloco do while else: contador em.:  {contador}")

print("=" *30)

print("fim programa")

print("=" *30)