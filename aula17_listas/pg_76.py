import os

# Limpa a tela
os.system('cls')

# Exibe a mensagem inicial
print('-' * 70)
print('SAÍDA COM FOR... ENUMERATE()')
print('-' * 70)

# Criando uma lista de números
lista_numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Inicializa a variável soma
soma = 0

# Percorrendo a lista com o enumerate()
# O comando enumerate adiciona um índice para cada valor de nossa lista
# O "start" é opcional, para não começar no índice 0
for indice, numero in enumerate(lista_numeros, start=1):
    soma += numero  # Soma os números
    print(f'Índice: {indice} Número: {numero}')

# Exibe a soma dos números
print('-' * 70)
print(f'A soma de todos os números é: {soma}')
print('-' * 70)

# Mensagem final
print('Fim do programa!')
