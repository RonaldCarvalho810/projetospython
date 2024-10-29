#Segundo essas políticas, viagens de até 200 km têm um custo de R$0,70 por km rodado, enquanto viagens acima dessa distância passam a custar R$0,40 por km rodado

import os


os.system("cls")

print("=" * 20)
print("modulo para calculo de valor de passagens..:")
print("=" * 20)

#definindo valores das mariaveis
valor_final = 0
kilometragem = 0
#entrada de dados
kilometragem = float(input("digite a kilometragem da  viagem..:"))

#calculando parametros
if (kilometragem <= 200):
    valor_final = kilometragem * 0.7
else:
    valor_final = kilometragem * 0.4

print("=" * 20)
print("resultado do calculo")
print(f"a viagem tem..: {kilometragem: .2f} km de deslocamento e seu valor por passagem é de..: {valor_final: .2f}")
print("=" * 20)
print()
