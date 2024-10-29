import os


os.system("cls")

print("=" * 20)
print("modulo para conferencia de velocidade..:")
print("=" * 20)

#definindo valores das mariaveis
velocidade = 0
situacao = ""


velocidade =int(input("digite a velocidade do veiculo..:"))


#conferindo se a velocidade entra dentro do permitido
if (velocidade < 60):
    situacao = " o veiculo esta abaixo do limite"
elif (velocidade == 60):
    situacao = "veiculo está no limite da pista"

else:
    situacao = "o veiculo esta acima do limite"

print("=" * 20)
print("resultado")
print(situacao)
print("=" * 20)
print()
