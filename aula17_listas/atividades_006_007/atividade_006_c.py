# Faça um programa que procure na lista numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] e produza:
# • O intervalo de 1 até 9
# • O intervalo de 8 até 13
# • Os números pares
# • Os números ímpares
# • Os múltiplos de 2, 3 e 4
# • Lista reversa
# • O produto dos intervalos 5-6 por 11-12

import os
os.system("cls")
numeros_pares = []
numeros_impares = []
multiplos_2 = []
multiplos_3 = []
multiplos_4 = []
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
intervalo1 = numeros[0:9]
intervalo2 = numeros[7:13]
for numero in range(0,len(numeros)):
    if numeros[numero]% 2 == 0:
        numeros_pares.append( numeros[numero])
        multiplos_2.append(numeros[numero])
        if numeros[numero] %4 ==0:
            multiplos_4.append (numeros[numero])
    else:
        numeros_impares.append (numeros[numero])
        if numeros[numero] %3 ==0:
            multiplos_3.append (numeros[numero])


inversa = numeros[::-1]
intervalo_5_11 = numeros[5] * numeros[11]
intervalo_6_12 = numeros[6] * numeros[12]
print(f"a lista original é.: {numeros}")
print(f"os numeros no intervalo de 1 a 9 são.: {intervalo1}")
print(f"os numeros no intervalo de 8 a 13 são.: {intervalo2}")
print(f" os numeros pares sao.: {numeros_pares}")
print(f" os numeros impares sao.: {numeros_impares}")
print(f"os numeros multiplos de 2 são.: {multiplos_2}")
print(f"os numeros multiplos de 3 são.: {multiplos_3}")
print(f"os numeros multiplos de 4 são.: {multiplos_4}")
print(f"a lista invertida é.: {inversa}")
print(f"o produto indice 5 * indice 11 é.: {intervalo_5_11}")
print(f"o produto indice6 * indice12 é.: {intervalo_6_12}")
