import os

os.system('cls')

historico = {
    "C1": [],
    "V1": [],
    "C2": [],
    "V2": []
}

while True:
    print('*' * 70)
    print("\nFórmula: C1 x V1 = C2 x V2")
    print("Digite os valores conhecidos e deixe o valor desconhecido vazio.")
    print("1. Calcular valor faltante")
    print("2. Mostrar histórico de cálculos")
    print("3. Sair")
    print('*' * 70)

    opcao = input("Escolha uma opção (1-3): ")

    if opcao == '1':
        try:
            dados = {}
            dados["C1"] = input("Digite o valor de C1 (ou deixe vazio): ")
            dados["V1"] = input("Digite o valor de V1 (ou deixe vazio): ")
            dados["C2"] = input("Digite o valor de C2 (ou deixe vazio): ")
            dados["V2"] = input("Digite o valor de V2 (ou deixe vazio): ")

            for chave in dados:
                dados[chave] = float(dados[chave]) if dados[chave] else None

            if list(dados.values()).count(None) != 1:
                print("Erro: Apenas um valor deve ser deixado vazio.")
                continue

            if dados["C1"] is None:
                dados["C1"] = (dados["C2"] * dados["V2"]) / dados["V1"]
                print(f"O valor de C1 é: {dados['C1']:.2f}")
            elif dados["V1"] is None:
                dados["V1"] = (dados["C2"] * dados["V2"]) / dados["C1"]
                print(f"O valor de V1 é: {dados['V1']:.2f}")
            elif dados["C2"] is None:
                dados["C2"] = (dados["C1"] * dados["V1"]) / dados["V2"]
                print(f"O valor de C2 é: {dados['C2']:.2f}")
            elif dados["V2"] is None:
                dados["V2"] = (dados["C1"] * dados["V1"]) / dados["C2"]
                print(f"O valor de V2 é: {dados['V2']:.2f}")

            for chave, valor in dados.items():
                historico[chave].append(valor)

        except ValueError:
            print("Erro: Certifique-se de digitar números válidos.")

    elif opcao == '2':
        print("\nHistórico de cálculos:")
        if any(historico[chave] for chave in historico):
            for i in range(len(historico["C1"])):
                print(
                    f"Cálculo {i + 1}: C1={historico['C1'][i]:.2f}, "
                    f"V1={historico['V1'][i]:.2f}, "
                    f"C2={historico['C2'][i]:.2f}, "
                    f"V2={historico['V2'][i]:.2f}"
                )
        else:
            print("Nenhum cálculo armazenado.")

    elif opcao == '3':
        print("Saindo do programa.")
        break

    else:
        print("Opção inválida. Tente novamente.")

    input("\nPressione Enter para continuar...")
    os.system('cls')
