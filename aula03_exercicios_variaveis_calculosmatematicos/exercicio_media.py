import os

os.system("cls")

nota1 = float(input("digite a 1ª nota..:"))
nota2 = float(input("digite a 2ª nota..:"))
nota3 = float(input("digite a 3ª nota..:"))
nota4 = float(input("digite a 4ª nota..:"))

soma = nota1 + nota2 + nota3 + nota4
media = nota1 + nota2 + nota3 + nota4 / 4
media_correta = (nota1 + nota2 + nota3 + nota4) / 4

#saida de dados

print("=" *20)
print("resultados")
print("=" *20)
print()

print(f"nota 01| {nota1} |nota 02| {nota2}| ")
print(f"nota 03| {nota3} |nota 04| {nota4}| ")
print(f"  total| {soma} |media errada| {media}| ")
print(f"media correta| {media_correta} ")
print()