import os

# Limpa o terminal
os.system('cls')

print("=" * 70)
print("ESTRUTURA DE DADOS: DICIONÁRIO")
print("=" * 70)

# Declarando dicionários
compras = {}
pessoas = {}
cores = {}
elementos = {}
numeros = {}

# Atribuindo valores
compras['id'] = 1
compras['item'] = 'Caderno'
compras['valor'] = 18.80

pessoas['id'] = '0010'
pessoas['nome'] = 'Sherlock Holmes'
pessoas['endereco'] = 'Baker Street'
pessoas['numero'] = 221
pessoas['cidade'] = 'Londres'
pessoas['pais'] = 'Inglaterra'

cores['red'] = 'Vermelho'
cores['green'] = 'Verde'
cores['blue'] = 'Azul'

elementos['Pb'] = 'Chumbo'
elementos['Au'] = 'Ouro'
elementos['N'] = 'Nitrogênio'

# Exibindo os dicionários
print("\nCompras:", compras)
print("Pessoas:", pessoas)
print("Cores:", cores)
print("Elementos:", elementos)

# Atribuindo valores ao dicionário 'numeros'
numeros[1] = 100
numeros[2] = 200
numeros[3] = 300

# Saída simples
print(f"Minhas compras: {compras}")
print(f"Detetives: {pessoas}")
print(f"Cor RGB: {cores}")
print(f"Tabela periódica: {elementos}")
print(f"Listagem de números: {numeros}")

# Exibindo separador final
print()
print("-" * 100)
