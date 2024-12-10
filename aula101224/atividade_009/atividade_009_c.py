# Desenvolva um programa que crie um dicionário contendo ferramentas, onde:

# O nome de cada ferramenta será a chave.
# O seu respectivo valor será uma breve descrição técnica.
# O programa deve permitir:

# Alterar o valor (descrição) de qualquer ferramenta já cadastrada.
# Após a criação e possível modificação do dicionário, o programa deve:
# Exibir o dicionário ordenado alfabeticamente pelos nomes das ferramentas.
# Mostrar a quantidade total de ferramentas cadastradas.
# Gerar um relatório indicando quantas ferramentas possuem mais de uma palavra no nome.

import os
os.system("cls")
ferramentas = {}

print("Bem-vindo ao gerenciador de ferramentas!")
print("Você pode cadastrar ferramentas, alterar descrições e gerar relatórios.")

while True:
    print("\nMenu:")
    print("1. Adicionar uma nova ferramenta")
    print("2. Alterar a descrição de uma ferramenta existente")
    print("3. Finalizar e exibir o relatório")
    opcao = input("Escolha uma opção (1, 2 ou 3): ")

    if opcao == "1":
        nome = input("Digite o nome da ferramenta: ").strip()
        if nome in ferramentas:
            print("Essa ferramenta já está cadastrada! Use a opção 2 para alterar a descrição.")
        else:
            descricao = input(f"Digite a descrição técnica para a ferramenta '{nome}': ").strip()
            ferramentas[nome] = descricao
            print(f"Ferramenta '{nome}' cadastrada com sucesso!")

    elif opcao == "2":
        nome = input("Digite o nome da ferramenta que deseja alterar: ").strip()
        if nome in ferramentas:
            nova_descricao = input(f"Digite a nova descrição para a ferramenta '{nome}': ").strip()
            ferramentas[nome] = nova_descricao
            print(f"Descrição da ferramenta '{nome}' alterada com sucesso!")
        else:
            print("Essa ferramenta não está cadastrada! Use a opção 1 para adicioná-la.")

    elif opcao == "3":
        print("\nExibindo o relatório final:")

        ferramentas_ordenadas = dict(sorted(ferramentas.items()))

        print("\nDicionário de ferramentas ordenado:")
        for nome, descricao in ferramentas_ordenadas.items():
            print(f"{nome}: {descricao}")

        print(f"\nTotal de ferramentas cadastradas: {len(ferramentas)}")

        ferramentas_multiplas_palavras = sum(1 for nome in ferramentas if len(nome.split()) > 1)
        print(f"\nQuantidade de ferramentas com mais de uma palavra no nome: {ferramentas_multiplas_palavras}")

        break  

    else:
        print("Opção inválida! Tente novamente.")
