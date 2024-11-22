import os

# Limpa a tela
os.system('cls')

# Lista original
lista = [1, 2, 3, 4]

# Mostrando a lista original
print("Lista original:", lista)

# Pedindo ao usuário o elemento a ser removido
elemento = input("Elemento a ser removido: ")

# Tentando remover o elemento da lista
if elemento.isdigit():  # Verifica se o valor é um número
    elemento = int(elemento)  # Converte para inteiro
    if elemento in lista:  # Verifica se o elemento está na lista
        lista.remove(elemento)  # Remove o elemento
        print("Lista após a remoção:", lista)
    else:
        print("Elemento não encontrado na lista.")
else:
    print("Entrada inválida. Por favor, insira um número.")
