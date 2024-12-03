import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect("c:\\banco\\teste.db")

# Criação de um cursor para executar comandos SQL
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT UNIQUE,
    endereco TEXT
)
""")

conn.commit()  # Salva as alterações
conn.close()

conn = sqlite3.connect("c:\\banco\\teste.db")
cursor = conn.cursor()

# Inserindo dados
cursor.execute("""
INSERT INTO clientes (nome, telefone, email, endereco) 
VALUES (?, ?, ?, ?)
""", ("João Silva", "123456789", "joao@email.com", "Rua A"))

conn.commit()
conn.close()

conn = sqlite3.connect("c:\\banco\\teste.db")
cursor = conn.cursor()

# Consultando dados
cursor.execute("SELECT * FROM clientes")
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

conn.close()
