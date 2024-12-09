import os

# Dicionário da agenda de contatos
agenda = {
    "Jojo": "99196-3038",
    "Dio": "99196-5050",
    "Jolyne": "99196-6060",
    "Lisa Lisa": "99196-7070",
    "Speedwagon": "99196-8888",
    "Zeppeli": "99196-9090",
    "Suzie Q": "99196-0000"
}

while True:
    os.system("cls")  # Limpa a tela (Windows)
    print("=" * 70)
    print("Agenda de Contatos:")
    for nome, telefone in agenda.items():
        print(f"{nome}: {telefone}")
    print("=" * 70)

    # Testes iniciais
    print("\nPrimeiro teste: Verificar se 'Jojo' está no dicionário.")
    if "Jojo" in agenda:
        print("VERDADEIRO! Jojo está no dicionário.")
    else:
        print("FALSO! Jojo não está no dicionário.")

    print("\nSegundo teste: Verificar se 'John' não está no dicionário.")
    if "John" not in agenda:
        print("VERDADEIRO! John não está no dicionário.")
    else:
        print("FALSO! John está no dicionário.")

    # Menu de opções
    print("=" * 70)
    print("Menu de opções:")
    print("1. Adicionar um contato")
    print("2. Remover um contato")
    print("3. Verificar contato específico")
    print("4. Mostrar agenda completa")
    print("5. Sair")
    print("=" * 70)

    opcao = input("Escolha uma opção (1-5): ")

    if opcao == '1':
        # Adicionar um contato
        nome = input("Digite o nome do contato: ")
        telefone = input("Digite o telefone do contato: ")
        agenda[nome] = telefone
        print(f"Contato {nome}: {telefone} adicionado.")

    elif opcao == '2':
        # Remover um contato
        nome = input("Digite o nome do contato que deseja remover: ")
        if nome in agenda:
            del agenda[nome]
            print(f"Contato {nome} removido.")
        else:
            print(f"Contato {nome} não encontrado na agenda.")

    elif opcao == '3':
        # Verificar contato específico
        nome = input("Digite o nome do contato que deseja verificar: ")
        if nome in agenda:
            print(f"Contato encontrado: {nome}: {agenda[nome]}")
        else:
            print(f"Contato {nome} não encontrado na agenda.")

    elif opcao == '4':
        # Mostrar agenda completa
        print("\nAgenda de Contatos:")
        for nome, telefone in agenda.items():
            print(f"{nome}: {telefone}")

    elif opcao == '5':
        # Sair do programa
        print("Saindo do programa.")
        break

    else:
        print("Opção inválida. Tente novamente.")

    # Pausa para o usuário ver as mensagens antes de limpar a tela
    input("\nPressione Enter para continuar...")
