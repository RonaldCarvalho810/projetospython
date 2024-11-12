import os
os.system("cls")

print("=" *30)
print("teste estrutura while else break")
print("=" *30)

print()


while (True):
    nome = str(input("digite um nome.: [s - para sair]")).lower()
    print(nome)
    if(nome != "s"):
        
        print("continue digitando")
    else:
        print("vc digitou s")
        break

print("=" *30)
print("final")
print("=" *30)