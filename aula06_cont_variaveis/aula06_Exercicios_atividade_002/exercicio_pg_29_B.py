#calcular:𝑥²−6𝑥+5 onde: 𝑥’ = 5 e 𝑥’’ = 1

import os


os.system("cls")

print("=" * 20)
print("modulo para calcular a equação (𝑥²−6𝑥+5) ")
print("=" * 20)
print("regra para calculo das raizes.: ax² + bx + c =0 ")
#atribuindo valores das mariaveis

a = 1
b = -6
c = 5
delta = 0
primeira_raiz = 0
segunda_raiz = 0

#calculando o delta

delta = b**2 - (4*a*c)

#print(f"o valor de delta é..: {delta}")

primeira_raiz = (-(b) + (delta **(1/2) )) / 2*a
segunda_raiz = (-(b) - (delta **(1/2) )) / 2*a

print("=" * 20)
print("resultado")
print("=" * 20)
print(f"as raizes da equação..: (𝑥²−6𝑥+5=0) são  𝑥’ ={primeira_raiz} e 𝑥’’ ={segunda_raiz} ")
print("=" * 20)
print()
