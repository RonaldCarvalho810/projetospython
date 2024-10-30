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
    situacao = " contiune dirigindo com seurança"
elif (velocidade == 60):
    situacao = "Atenção: vc atingiu o limite de velocidade da pista"

else:
    situacao = "o veiculo esta acima do limite"

print("=" * 20)
print("resultado")
print(situacao)
print("=" * 20)
print()
