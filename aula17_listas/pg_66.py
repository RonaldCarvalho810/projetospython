import os
os.system("cls")

# Lista original
print("ESTRUTURA DE DADOS: LISTAS")
lista = [1, 2, 3, 4]  # Lista inicial

# Pedindo ao usuário para fornecer a posição e o elemento a ser inserido
posicao = int(input("Posição onde deseja inserir o elemento: "))
elemento = input("Elemento a ser inserido: ")

# Verificando se a posição fornecida pelo usuário é válida
if 0 <= posicao < len(lista):
    # Inserindo o elemento na lista na posição especificada pelo usuário
    lista.insert(posicao, elemento)
    print("Lista após a inserção:", lista)
else:
    print(f"Posição fora do intervalo 0 a {len(lista)}")

print("Fim do programa.")
