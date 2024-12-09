import os

os.system('cls')

elementos = {}
tabela_periodica = []

for i in range(2):
    print(f"Entrada de dados ({i+1}):")
    simbolo = input("Símbolo do elemento: ")
    nome = input("Nome do elemento: ")
    
    elementos['simbolo'] = simbolo
    elementos['nome'] = nome

    tabela_periodica.append(elementos.copy())
    print()

print("=" * 70)
print("Elementos da tabela periódica:")
print(tabela_periodica)
print("=" * 70)
print()

print("Detalhes dos elementos:")
print("=" * 70)
for elemento in tabela_periodica:  
    for chave, valor in elemento.items():  
        print(f"{chave.capitalize()}: {valor}")
    print("=" * 70)  
