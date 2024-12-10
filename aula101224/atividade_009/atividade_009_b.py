# Crie um programa quecomece com 5 cores como chaves e permita ao usuário controlar descrições ou códigos de cores.
# O programa deve oferecer as seguintes funcionalidades:

# Adicionar novas cores com suas respectivas descrições.
# Modificar o valor (descrição) de uma cor já existente.
# Após a criação e possível modificação do dicionário, o programa deve:

# Exibir o dicionário de forma ordenada alfabeticamente pelas chaves.
# Mostrar a quantidade total de cores cadastradas.
# Exibir quantas cores possuem nomes que começam com cada letra inicial.


import os
os.system("cls")
cores = {
    "vermelho": "cor quente, associada à paixão",
    "azul": "cor fria, simboliza tranquilidade",
    "verde": "cor da natureza, transmite esperança",
    "amarelo": "cor brilhante, representa energia",
    "preto": "cor neutra, simboliza elegância"
}

print("Bem-vindo ao gerenciador de cores!")
print("Você pode adicionar novas cores ou modificar as descrições das cores existentes.")

while True:
    print("\nMenu:")
    print("1. Adicionar uma nova cor")
    print("2. Modificar a descrição de uma cor existente")
    print("3. Finalizar e exibir o relatório")
    opcao = input("Escolha uma opção (1, 2 ou 3): ")

    if opcao == "1":
        nova_cor = input("Digite o nome da nova cor: ").lower()
        if nova_cor in cores:
            print("Essa cor já existe no dicionário! Use a opção 2 para modificar sua descrição.")
        else:
            descricao = input(f"Digite a descrição para a cor '{nova_cor}': ")
            cores[nova_cor] = descricao
            print(f"Cor '{nova_cor}' adicionada com sucesso!")

    elif opcao == "2":
        cor_existente = input("Digite o nome da cor que deseja modificar: ").lower()
        if cor_existente in cores:
            nova_descricao = input(f"Digite a nova descrição para a cor '{cor_existente}': ")
            cores[cor_existente] = nova_descricao
            print(f"Descrição da cor '{cor_existente}' modificada com sucesso!")
        else:
            print("Essa cor não está cadastrada! Use a opção 1 para adicioná-la.")

    elif opcao == "3":
        print("\nExibindo o relatório final:")
        
        cores_ordenadas = dict(sorted(cores.items()))

        print("\nDicionário de cores ordenado:")
        for cor, descricao in cores_ordenadas.items():
            print(f"{cor}: {descricao}")

        print(f"\nTotal de cores cadastradas: {len(cores)}")

        iniciais = {}
        for cor in cores:
            inicial = cor[0].upper()
            iniciais[inicial] = iniciais.get(inicial, 0) + 1

        print("\nQuantidade de cores por inicial:")
        for inicial, quantidade in sorted(iniciais.items()):
            print(f"{inicial}: {quantidade} cor(es)")

        break 

    else:
        print("Opção inválida! Tente novamente.")
