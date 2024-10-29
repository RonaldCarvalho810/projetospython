#Crie um programa que converta uma medida em metros para centímetros e milímetros.

import os

os.system("cls")

num1 = float(input("digite o a medida em metros..: "))

centimetros = float(num1 * 100)
milimetros = float(num1 * 1000)


print (f"a medida base é..:{num1} m, sua conversão em centimetros É..:{centimetros} cm e em milimetros É..: {milimetros} mm")
