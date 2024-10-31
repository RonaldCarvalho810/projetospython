#modulo para calcular media

def calcular_media(numeros):

    if len(numeros) == 0:
        return 0  

    soma = sum(numeros)
    media = soma / len(numeros)
    return media
