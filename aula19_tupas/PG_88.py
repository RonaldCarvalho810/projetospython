import os
os.system('cls')

# Solicitar ao usuário a quantidade de elementos na tupla
numero_elementos = int(input("Quantos elementos na tupla? "))

# Inicializar uma lista vazia para coletar os elementos
elementos = []

# Estrutura de repetição para preencher a lista
for i in range(numero_elementos):
    while True:
        valor = input(f"Digite o valor {i + 1} de {numero_elementos}: ")
        if valor.isdigit():  # Verificar se a entrada é um número
            elementos.append(int(valor))  # Adicionar à lista como inteiro
            break
        else:
            print("Entrada inválida. Digite um número.")

# Converter a lista para tupla
tupla = tuple(elementos)

# Exibir a tupla criada
print("=" * 70)
print(f"Tupla criada: {tupla}")
print("=" * 70)

# Estrutura de repetição para operações até que o usuário escolha sair
while True:
    # Verificar se um número está na tupla
    valor = int(input("Verificar se o número está na tupla: "))
    if valor in tupla:
        print(f"O número {valor} está na tupla.")

        # Contar quantas vezes o número aparece
        contagem = tupla.count(valor)
        print(f"O número {valor} aparece {contagem} vez(es).")

        # Encontrar o índice da primeira ocorrência
        indice = tupla.index(valor)
        print(f"A 1ª ocorrência de {valor} está no índice {indice}.")
    else:
        print(f"O número {valor} não está na tupla.")

    # Perguntar ao usuário se deseja continuar ou sair
    continuar = input("Deseja continuar? (s/n): ").lower()
    if continuar != 's':
        print("Encerrando o programa. Até mais!")
        break
    print("=" * 70)

print("Fim do programa!")
