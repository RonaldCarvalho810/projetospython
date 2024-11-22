import os

# Limpa a tela
os.system("cls")

# Exibe a mensagem inicial
print('-' * 70)
print('SAÍDA COM IN E NOT IN')
print('-' * 70)

# Exemplo 1: Verificando a presença de um número na lista
lista_numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(lista_numeros)

# Verificando se o número 3 está na lista
if 3 in lista_numeros:
    posicao = lista_numeros.index(3)
    print(f'O número 3 está na posição {posicao}')
else:
    print('O número 3 não está na lista')

# Exemplo 2: Verificando se um nome está na lista
lista_nomes = ['John', 'Jane', 'Carol']
print(lista_nomes)

# Verificando se 'Maria' não está na lista
if 'Maria' not in lista_nomes:
    lista_nomes.append('Maria')
    print("\nO nome 'Maria' foi acrescentado")
else:
    print("O nome 'Maria' já está na lista")

# Exibindo a lista atualizada
print(lista_nomes)

# Finalizando o programa
print('-' * 70)
print("Fim do programa!")
print('-' * 70)
