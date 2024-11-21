import os

os.system('cls')

posicoes = []
quantidade = 0

entrada = input("Digite números separados por espaço: ")

numeros_str = entrada.split()

numeros = []
for num_str in numeros_str:
    numeros.append(int(num_str))

busca_numero = int(input("Digite o número que deseja encontrar: "))

if busca_numero in numeros:
    quantidade  = numeros.count(busca_numero)
    print(quantidade)
    for interno in range (0,quantidade): 
        indice = numeros.index(busca_numero)
        posicoes.insert(0,indice)
    print(f"O número {busca_numero} está nos índices {posicoes}.")
else:
    #print(posicoes)
    print(f"O número {busca_numero} não foi encontrado na lista.")

print(f"Lista fornecida: {numeros}")
