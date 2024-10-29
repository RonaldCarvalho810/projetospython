def calcular_media(numeros):
    """
    Calcula a média de uma lista de números.
    :param numeros: lista de números (int ou float)
    :return: média dos números
    """
    if len(numeros) == 0:
        return 0  # Evita divisão por zero

    soma = sum(numeros)
    media = soma / len(numeros)
    return media