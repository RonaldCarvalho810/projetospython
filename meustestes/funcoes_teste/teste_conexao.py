#C:\Ronald\banco\bnc_dds.mdb
import pyodbc

# Caminho do arquivo .mdb
db_path = r"C:\Ronald\banco\bnc_dds.mdb"

# Conexão com o banco de dados
conn = pyodbc.connect(
    f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};"
)

# Cursor para executar comandos SQL
cursor = conn.cursor()

# Comando SQL para inserir dados
sql_insert = "INSERT INTO NomeDaTabela (Coluna1, Coluna2) VALUES (?, ?)"
valores = ("Valor1", "Valor2")

cursor.execute(sql_insert, valores)
conn.commit()  # Confirma as alterações

print("Dados inseridos com sucesso!")

# Fechar a conexão
conn.close()
