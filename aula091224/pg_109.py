import os

os.system('cls')

elementos = {}
tabela_periodica = []

while True:
    os.system('cls')

    print("=" * 70)
    print("MENU DE OPÇÕES:")
    print("=" * 70)
    print("1. Adicionar um elemento")
    print("2. Visualizar todos os elementos")
    print("3. Atualizar um elemento")
    print("4. Remover um elemento")
    print("5. Sair")
    print("=" * 70)

    opcao = input("Escolha uma opção (1-5): ")

    if opcao == '1':  # Adicionar um elemento
        simbolo = input("Símbolo do elemento: ")
        nome = input("Nome do elemento: ")
        elementos['simbolo'] = simbolo
        elementos['nome'] = nome
        tabela_periodica.append(elementos.copy())
        input("\nElemento adicionado. Pressione Enter para continuar.")

    elif opcao == '2':  # Visualizar todos os elementos
        os.system('cls')
        print("=" * 70)
        print("ELEMENTOS DA TABELA PERIÓDICA:")
        print("=" * 70)
        for elemento in tabela_periodica:
            for chave, valor in elemento.items():
                print(f"{chave.capitalize()}: {valor}")
            print("-" * 70)
        input("\nPressione Enter para voltar ao menu.")

    elif opcao == '3':  # Atualizar um elemento
        os.system('cls')
        simbolo = input("Informe o símbolo do elemento que deseja atualizar: ")
        encontrado = False
        for elemento in tabela_periodica:
            if elemento['simbolo'] == simbolo:
                novo_nome = input(f"Digite o novo nome para o elemento '{simbolo}': ")
                elemento['nome'] = novo_nome
                encontrado = True
                print("\nElemento atualizado com sucesso!")
                break
        if not encontrado:
            print("\nElemento não encontrado.")
        input("\nPressione Enter para continuar.")

    elif opcao == '4':  # Remover um elemento
        simbolo = input("Digite o símbolo do elemento que deseja remover: ")
        encontrado = False  # Inicializa a flag como False
        for elemento in tabela_periodica:
            if elemento['simbolo'] == simbolo:  # Verifica se o símbolo corresponde
                tabela_periodica.remove(elemento)  # Remove o elemento da lista
                encontrado = True  # Define a flag como True quando o elemento é encontrado
                break
        if encontrado:
            input("\nElemento removido. Pressione Enter para continuar...")
        else:
            input("\nElemento não encontrado. Pressione Enter para continuar...")

    elif opcao == '5':  # Sair do programa
        print("\nSaindo do programa...")
        break

    else:  # Opção inválida
        input("\nOpção inválida. Pressione Enter para tentar novamente...")
