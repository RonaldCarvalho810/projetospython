#Implemente um programa que receba um número inteiro e imprima sua tabuada de multiplicação.

import os

os.system("cls")

num1 = int(input("digite o a medida em metros..: "))

t1 = int(num1 * 1)
t2 = int(num1 * 2)
t3 = int(num1 * 3)
t4 = int(num1 * 4)
t5 = int(num1 * 5)
t6 = int(num1 * 6)
t7 = int(num1 * 7)
t8 = int(num1 * 8)
t9 = int(num1 * 9)
t10 = int(num1 * 10)

print (f"o numero base é..:{num1} , sua tabuada é..:")
print(f"| x1 = {t1}| x2 = {t2}| x3 = {t3} ")
print(f"| x4 = {t4}| x5 = {t5}| x6 = {t6} ")
print(f"| x7 = {t7}| x8 = {t8}| x9 = {t9} ")
print(f"| x10 = {t10}")