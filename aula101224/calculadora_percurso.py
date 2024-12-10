import os
os.system("cls")

print("Bem-vindo ao cálculo de valor de deslocamento!")
print("Escolha o tipo de viagem:")
print("1. Viagem dentro da cidade")
print("2. Viagem intermunicipal")

tipo_viagem = input("Digite 1 para viagem na cidade ou 2 para viagem intermunicipal: ")

km = float(input("Digite a distância em quilômetros: "))

if tipo_viagem == "1":
    valor_km = float(input("Digite o valor do km: "))
    valor_total = valor_km * km
    print(f"O valor total do deslocamento na cidade é: R${valor_total:.2f}")

elif tipo_viagem == "2":
    valor_km = float(input("Digite o valor do km: "))
    valor_total = (valor_km * km * 2)
    print(f"O valor total da viagem intermunicipal é: R${valor_total:.2f}")

else:
    print("Opção inválida! Tente novamente.")
