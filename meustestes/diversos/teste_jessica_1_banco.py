import os
os.system("cls")

# for a in range(1,5):
#     for b in range(1,5):
#         for c in range(1,5):
#             print(f"{a}{b}{c}", end="|")

produtos = {
    "001": {"produto": "camisa", "preco": 10.50, "estoque": 100},
    "002": {"produto": "tenis", "preco": 100.70, "estoque": 100},
    "003": {"produto": "calca", "preco": 70.00, "estoque": 100}
}

#print(produtos)

nome_procurado = input("Digite o código do produto: ")

if nome_procurado in produtos:
    produto = produtos[nome_procurado]
    print(f"Encontrado: Código: {nome_procurado}, Produto: {produto['produto']}, Preço: R${produto['preco']:.2f}, Estoque: {produto['estoque']}")
    
    alterar_estoque = input("Deseja alterar o estoque? (s/n): ").lower()
    
    if alterar_estoque == "s":
        try:
            quantidade = int(input("Digite a quantidade para ajustar (+ para adicionar, - para remover): "))
            novo_estoque = produto["estoque"] + quantidade
            
            if novo_estoque < 0:
                print("Erro: o estoque não pode ficar negativo!")
            else:
                produto["estoque"] = novo_estoque
                print(f"Estoque atualizado: {produto['estoque']} unidades.")
        except ValueError:
            print("Erro: digite um número válido para a quantidade.")
else:
    print("Produto não encontrado!")

print("\nProdutos atualizados:")
print(produtos)


