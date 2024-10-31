import os

os.system("cls")

print("=" *20)
print(" calculadora de juros compostos")
print("=" *20)

investimento = float(input("digite o investimento inicial..:") )
periodo = float(input("digite o periodo, em meses..:") )
juros = float(input("digite a taxa de juros..:") )

porcentagem = juros / 100

montante = investimento*((1+porcentagem)**periodo)
formatado = f"{montante:.2f}"

print("=" *20)
print(f" o montante de uma aplicacao de {investimento}, por {periodo} meses com uma taxa de {juros} por cento é: {formatado}")
print("=" *20)