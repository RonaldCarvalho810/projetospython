# testando função media

import meu_modulo_media

nummero1 = int(input("Digite o primeiro numero"))
nummero2 = int(input("Digite o segundo numero"))
nummero3 = int(input("Digite o terceiro numero"))
nummero4 = int(input("Digite o quarto numero"))
nummero5 = int(input("Digite o quinto numero"))


numeros = [nummero1, nummero2, nummero3, nummero4, nummero5]

# Calculando a média usando a função do meu módulo
media = meu_modulo_media.calcular_media(numeros)
print(f"A média dos números é: {media:.2f}")
