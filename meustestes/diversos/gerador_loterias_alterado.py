#gera numeros dentro dos parametros especificados
import os
import random
os.system("cls")

primeiro = int(input("Digite o primeiro número: "))
ultimo = int(input("Digite o último número: "))
rodadas = int(input("Digite a quantidade de rodadas: "))
quantidade_dezenas = int(input("Digite a quantidade de dezenas: "))

lista_original = []
for numero in range(primeiro, ultimo + 1):
    lista_original.append(numero)

for interno1 in range(rodadas):
    lista = lista_original[:]
    dezenas_selecionadas = []
    
    for _ in range(quantidade_dezenas):
        random.shuffle(lista)
        escolhido = lista.pop(0)
        dezenas_selecionadas.append(escolhido)
    
    dezenas_selecionadas = sorted(dezenas_selecionadas)
    print(f"Rodada {interno1 + 1}: ", " ".join(map(lambda num: f"{num:02}", dezenas_selecionadas)))
