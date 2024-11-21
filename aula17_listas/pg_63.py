import os
os.system('cls') 
print(76) 
print('ESTRUTURA DE DADOS: LISTAS [ ]') 
print('=' *78) 
lista_mista = ['a', 'b', 3, 'John', 'e', 500, 'g', 'h'] 
lista_fatiadal =  lista_mista[0] 
lista_fatiada2 =  lista_mista[:] #Fatia os elementos do indice e até o indice 6 
lista_fatiada3 =  lista_mista [0:6] #Fatia os elementos do indice e até o indice 6 de 2 en 2 lista fatiada4 
lista_fatiada4 = lista_mista [0:6:2] #Fatia os elemeritos da direita para esquerda 
lista_fatiada5 =  lista_mista[::-1] 
print(f'1- Fatiando uma Lista: {lista_fatiadal}\n') 
print(f'2- Fatiando uma Lista: {lista_fatiada2}\n') 
print(f'3- Fatiando uma Lista: {lista_fatiada3}\n') 
print(f'4- Fatiando uma Lista: {lista_fatiada4}\n') 
print(f'5- Fatiando uma Lista: {lista_fatiada5}') 
print("-" *70) 
print('Fim do programal') 
print('-'*78)