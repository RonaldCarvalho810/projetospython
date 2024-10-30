#calcular:𝑥²−6𝑥+5 onde: 𝑥’ = 5 e 𝑥’’ = 1

import os


os.system("cls")

print("=" * 20)
print("modulo para calcular a equação (x²-6x+5) ")
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

primeira_raiz = (-(b) + (delta **(1/2) )) / 2*a
segunda_raiz = (-(b) - (delta **(1/2) )) / 2*a

print("=" * 20)

print("=" * 20)
print(f"as raizes da equação..: (x²-6x+5=0) são  x¹={primeira_raiz} e x²={segunda_raiz} ")
print("=" * 20)
print()
