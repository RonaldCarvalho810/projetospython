import os

os.system("cls")

clientes = {}
servicos = {}
agenda = {}

codigo_atual = 1

while len(clientes) < 5:
    print(f"\nCadastro do cliente {len(clientes) + 1} de 5:\n")
    
    codigo = str(codigo_atual)  
    codigo_atual += 1  
    
    nome = input("Digite o nome: ")
    telefone = input("Digite o telefone: ")
    email = input("Digite o email: ")
    
    clientes[codigo] = {
        "nome": nome,
        "telefone": telefone,
        "email": email
    }

    print(f"Cliente {nome} cadastrado com sucesso!")

print("\n--- Clientes cadastrados ---\n")
for codigo, dados in clientes.items():
    print(f"Código: {codigo}")
    print(f"Nome: {dados['nome']}")
    print(f"Telefone: {dados['telefone']}")
    print(f"Email: {dados['email']}")
    print("-" * 30)
