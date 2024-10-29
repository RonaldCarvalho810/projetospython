import os
os.system("cls)")

a = 10
b = 5
c = "josé"
d = "josé"

print("=" * 20)
print("condicionais operaionais relacionais")
print("=" * 20)

if c == d:
    print("=" * 20)
    print(f"{c} é igual a: {d}")
    print("=" * 20)
else:
    print(f"{c} não é igual a: {d}")

if a != c:
    print("=" * 20)
    print(f"{a} é diferente de: {c}")
    print("=" * 20)
else:
    print(f"{a} não é diferente de: {c}")

if a > b:
    print("=" * 20)
    print(f"{a} é maior que: {b}")
    print("=" * 20)
else:
    print(f"{a} não é maior que: {b}")

if b < a:
    print("=" * 20)
    print(f"{b} é menor que: {a}")
    print("=" * 20)
else:
    print(f"{b} não é menor que: {a}")

if a >= b:
    print("=" * 20)
    print(f"{a} é maior ou igual a: {b}")
    print("=" * 20)
else:
    print(f"{a} não é maior ou igual a: {b}")

if b <= a:
    print("=" * 20)
    print(f"{b} é menor ou igual a: {a}")
    print("=" * 20)
else:
    print(f"{b} não é menor ou igual a: {a}")


print("=" * 20)
print("fim do programa")
print("=" * 20)
print()