import os

# Limpa a tela
os.system('cls')

# Exibe mensagem inicial
print('SAÍDA COM FOR')
print('-' * 70)

# Criando uma lista
lista_alunos = []

# Pedindo ao usuário para inserir os nomes dos alunos
for c in range(0, 5):
    nome = str(input('Entre com o nome do aluno: '))  # Guardando em uma lista
    lista_alunos.append(nome)

# Exibindo os nomes dos alunos
print()
print('Impressão dos nomes de alunos:')

# Utilizando o len() para saber a quantidade de alunos e imprimir
for aluno in range(len(lista_alunos)):
    print(lista_alunos[aluno], end=' ')
    if aluno == 3:  # Condição para inserir quebra de linha após o 4º aluno
        print()  # Faz a quebra de linha

# Exibe a mensagem final
print()
print('-' * 70)
print('Fim do programa!')
