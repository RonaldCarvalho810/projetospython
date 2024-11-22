import os

# Limpa a tela
os.system('cls')

# Exibe a mensagem inicial
print('-' * 78)
print('VARRENDO LISTAS DENTRO DE LISTAS')
print('-' * 78)

# Criando uma lista 3x3 representando um jogo da velha
jogo_velha = [
    ['x', '0', 'X'],
    ['x', 'x', 'o'],
    ['0', '0', '0']
]

# Exibindo o tabuleiro do jogo da velha
print(jogo_velha)
print()

# Pegando manualmente os valores
print(f'Na linha 1, coluna 1, existe um: {jogo_velha[0][0]}')
print(f'Na linha 2, coluna 3, existe um: {jogo_velha[1][2]}')
print()

# Varrendo a lista com for e range
print('Varrendo a lista com um laço for:')
for linha in range(len(jogo_velha)):  # Acesso às linhas
    for coluna in range(len(jogo_velha[linha])):  # Acesso às colunas de cada linha
        print(jogo_velha[linha][coluna], end=' ')
    print()  # Para quebrar a linha após cada linha do tabuleiro

# Finalizando a execução
print('-' * 78)
