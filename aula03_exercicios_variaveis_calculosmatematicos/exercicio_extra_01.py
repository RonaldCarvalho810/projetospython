import os

os.system ("cls")


ano_base = 12
veiculo_base = "gol"
media_base = 10
injecao_base = True

print("veiculo base")
print('a variavel veiculo é do tipo:' , type(veiculo_base))
print('a variavel ano é do tipo:' , type(ano_base))
print('a variavel media é do tipo:' , type(media_base))
print('a variavel injecao é do tipo:' , type(injecao_base))

ano = int(input("digite o ano do carro..."))
veiculo = input("digite o modelo do carro...")
media = float(input(" digite a media do veiculo...:"))
injecao = input("digite o tipo de injecao...:")

print(f"variavel ano carro base é tipo:", type ({ano_base}))