import os 
import json

# Dados iniciais
produtos = {
    "001": {"produto": "camisa", "preco": 10.50, "estoque": 100},
    "002": {"produto": "tenis", "preco": 100.70, "estoque": 100},
    "003": {"produto": "calca", "preco": 70.00, "estoque": 100}
}

# Função para salvar os dados no arquivo txt
def salvar_dados(produtos, arquivo="produtos.txt"):
    with open(arquivo, "w") as f:
        json.dump(produtos, f)
    print("Dados salvos com sucesso!")

# Função para carregar os dados do arquivo txt
def carregar_dados(arquivo="produtos.txt"):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo não encontrado. Usando dados padrão.")
        return produtos  # Retorna os dados iniciais caso o arquivo não exista

# Carregar os dados (se houver um arquivo existente)
produtos = carregar_dados()

# Exibir os produtos
print("Produtos disponíveis:")
for codigo, dados in produtos.items():
    print(f"Código: {codigo}, Produto: {dados['produto']}, Preço: R${dados['preco']:.2f}, Estoque: {dados['estoque']}")

# Alterar estoque de um produto
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

print("Salvando arquivo em:", os.path.abspath("produtos.txt"))
# Salvar os dados atualizados no arquivo
salvar_dados(produtos)

# Exibir produtos atualizados
print("\nProdutos atualizados:")
for codigo, dados in produtos.items():
    print(f"Código: {codigo}, Produto: {dados['produto']}, Preço: R${dados['preco']:.2f}, Estoque: {dados['estoque']}")
