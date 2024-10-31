# funcção juros compostos

def juros_compostos( investimento, periodo, juros):

    porcentagem = juros / 100
    #calculando os juros
    
    montante = investimento*((1+porcentagem)**periodo)
    return montante