import os
import random
os.system("cls")

#inicio freeze
'''
def gerar_escala_formatada(texto):
    # Criar uma lista para armazenar os índices
    indices = []

    # Iterar sobre o texto e coletar os índices dos caracteres
    for i, letra in enumerate(texto):
        indices.append(i)

    # Construir a linha com os caracteres do texto
    linha_texto = " ".join(texto)

    # Criar a primeira linha (dezenas) e a segunda linha (unidades)
    linha_dezenas = [str(i // 10) for i in indices]  # Parte das dezenas
    linha_unidades = [str(i % 10) for i in indices]  # Parte das unidades

    # Converter as listas para string e juntar com espaços
    linha_dezenas = " ".join(linha_dezenas)
    linha_unidades = " ".join(linha_unidades)

    # Retornar as duas linhas formatadas
    return linha_dezenas, linha_unidades, linha_texto

# Exemplo de uso
texto = input("digite um texto.: ")
linha_dezenas, linha_unidades, linha_texto = gerar_escala_formatada(texto)

# Mostrar o resultado
print(linha_dezenas)
print(linha_unidades)
print(linha_texto)
'''
#termino freeze

#continuando o teste

numero = 0
numero2 = 0

nome = input("digite seu nome>: ")
variavel_dividida = list(nome)
meio = len(variavel_dividida)// 2

print(variavel_dividida)
print(meio)
print(variavel_dividida[meio])

numero = random.randint(1,25)
numero2 = random.uniform(1,25)

chave = "jose" in nome

if(chave == True):
    print("existe")

else:
    print("inexistente")
print(numero)
print(f"{numero2: .2f}")

