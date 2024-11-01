#testeando função juros compostos
import os
import meu_modulo_juros_compostos

os.system("cls")

investimento = float(input("digite o investimento inicial..: "))
periodo = int(input("digite o periodo da aplicação..: "))
juros = float(input("digite o juros mensal da aplicação..: "))

montante_final = meu_modulo_juros_compostos.juros_compostos(investimento, periodo, juros)

print(f" o valor final desse investimento será..: {montante_final:.2f}")

