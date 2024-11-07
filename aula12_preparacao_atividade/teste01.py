import os
os.system("cls")
print("teste")

#declarando variaveis:
frase = ""
parcial_frase = ""
primeiro_nome = ""
localizar = ""
contador = 0
ultimo_nome = ""
contador_lista = 0

#entrada de dados / atribuicao de variaveis:
frase = input("digite seu texto>: ")

maiusculo = frase.upper()
minusculo = frase.lower()

parcial_frase = frase [3:]

lista = frase.split(" ")
primeiro_nome = lista[0]
localizar = frase.find("a")
contador = frase.count("carvalho")
contador_lista = lista.count("almeida")
ultimo_nome = lista[len(lista)-1]

print("=" *20)
print("saídas")
print(lista)
print(parcial_frase)
print(maiusculo)
print(minusculo)
print(primeiro_nome)
print(ultimo_nome)
print(localizar)
print(contador)
print(contador_lista)
print("=" *20)