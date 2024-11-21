import os
os.system("cls")

print("=" *30)
print("teste de listas")
print("=" *30)

listas_numeros_inteiros = [1,2,3,4]
lista_vogais = ["a","e","i","o","u"]
listas_nomes = ["john" , "jane", "carol"]
lista_hegemonia = ["john,",80,1.90, "AB"]
lista_interna = [[1,2,3,4], ["a","e","i","o","u"]]

print(listas_numeros_inteiros)
print(lista_vogais)
print(listas_nomes)
print(lista_hegemonia)
print(lista_interna)

lista_num_indice_0 = listas_numeros_inteiros[0]
lista_vogais_indice_1 = lista_vogais[1]
listas_nomes_indice_2 = listas_nomes[2]
lista_hegemonia_indice_3 = lista_hegemonia[3]
lista_num_indice_1 = lista_interna[1]
teste_lista_interna= lista_interna[1][2]

print("=" *30)
print("ACESSANDO ELEMENTOS DA LISTA ")
print("=" *30)
print(f"lista de numeros>: {lista_num_indice_0}")
print(f"lista de vogais: {lista_vogais_indice_1}")
print(f"lista de nomes: {listas_nomes_indice_2}")
print(f"lista heterogenia>: {lista_hegemonia_indice_3}")
print(f"lista de interna>: {lista_num_indice_1}")
print(f"teste de indice lista interna>: {teste_lista_interna}")