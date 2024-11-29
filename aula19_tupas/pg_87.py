import os
os.system('cls')

# Lista de nomes
nomes = ['Agata', 'Bia', 'Coly', 'Isis']

# Iterar pela lista de nomes
for indice, nome in enumerate(nomes):
    # Criar uma tupla contendo o índice e o nome da pessoa atual
    minha_tupla = (indice, nome)
    
    # Exibir as informações usando a tupla e as variáveis diretamente
    print(f"O nome: {minha_tupla[1]}, posição: {minha_tupla[0]} da lista.")
    print(f"O nome: {nome}, posição: {indice} da lista.")
    print('-' * 70)
