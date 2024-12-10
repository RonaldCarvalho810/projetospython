# Parte 1: Criar e Ordenar um Dicionário
# Faça um programa para criar um dicionário com pelo menos quatro elementos. O programa deve permitir que o usuário insira as chaves e os valores.

# Chaves: Devem ser únicas, e o programa deve garantir isso.
# Após inserir todos os elementos, o programa deve exibir o dicionário ordenado pelas chaves.

import os
os.system("cls")

dicionario = {}

print("Vamos criar um dicionário com pelo menos 4 elementos.")

while len(dicionario) < 4:
    chave = input("Digite a chave (deve ser única): ")
    if chave in dicionario:
        print("Essa chave já existe! Tente novamente.")
    else:
        valor = input(f"Digite o valor para a chave '{chave}': ")
        dicionario[chave] = valor

dicionario_ordenado = dict(sorted(dicionario.items()))

print("\nDicionário ordenado pelas chaves:")
for chave, valor in dicionario_ordenado.items():
    print(f"{chave}: {valor}")

print("fim do programa")