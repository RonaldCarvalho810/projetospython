import random

def gerar_paginas():
    descricoes = [
        "Você está em uma floresta sombria, ouvindo os sons de criaturas ao longe.",
        "Um rio barulhento bloqueia o caminho à sua frente.",
        "Você encontra uma caverna escura, com vento soprando por dentro.",
        "Há uma torre misteriosa visível no horizonte.",
        "O chão sob seus pés parece frágil, como se pudesse ceder a qualquer momento.",
        "Você encontra um mapa rasgado em uma pedra.",
        "Um velho sábio aparece do nada, oferecendo conselhos.",
        "Há uma bifurcação no caminho: um lado está iluminado, o outro está escuro.",
        "Você vê pegadas frescas no chão, levando para o leste.",
        "Uma porta antiga aparece diante de você, coberta por runas mágicas.",
        "Você sente que está sendo observado, mas não vê ninguém por perto.",
        "Uma ponte de corda atravessa um precipício profundo.",
        "Uma cabana de madeira em ruínas surge no caminho.",
        "Um som de tambores tribais ressoa ao longe.",
        "Você encontra uma chave dourada em um tronco oco.",
        "Uma armadilha é disparada, mas você consegue desviar a tempo.",
        "Há um baú trancado no centro de um pequeno altar.",
        "O céu acima se torna vermelho, como se uma tempestade estivesse se formando.",
        "Uma escada de pedra leva a uma porta no topo de uma colina.",
        "Você encontra um diário velho e empoeirado com histórias intrigantes."
    ]

    paginas = {}
    for i in range(1, 301):
        descricao = descricoes[i % len(descricoes)]  # Escolhe uma descrição baseada no índice
        descricao = f"Página {i}: {descricao}"  # Adiciona o número da página para identificação

        opcoes = {}
        if i < 300:
            # Opção 1: Próxima página
            opcoes["1"] = {"texto": f"Ir para a página {i + 1}", "proxima_pagina": i + 1}
            # Opção 2: Salto de 10 páginas ou até a última página
            proxima_pagina = min(i + 10, 300)
            opcoes["2"] = {"texto": f"Ir para a página {proxima_pagina}", "proxima_pagina": proxima_pagina}

        if i == 300:
            descricao = "Parabéns! Você encontrou o grande tesouro e venceu a aventura!"

        paginas[i] = {"descricao": descricao, "opcoes": opcoes}

    return paginas

def jogo_aventura():
    paginas = gerar_paginas()
    pagina_atual = 1

    while True:
        print("\n" + paginas[pagina_atual]["descricao"])

        if not paginas[pagina_atual]["opcoes"]:
            print("Fim do jogo.")
            break

        print("\nEscolha:")
        for opcao, detalhe in paginas[pagina_atual]["opcoes"].items():
            print(f"{opcao}: {detalhe['texto']}")

        escolha = input("\nDigite o número da sua escolha: ")

        if escolha in paginas[pagina_atual]["opcoes"]:
            pagina_atual = paginas[pagina_atual]["opcoes"][escolha]["proxima_pagina"]
        else:
            print("Escolha inválida. Tente novamente.")

# Inicia o jogo
jogo_aventura()
