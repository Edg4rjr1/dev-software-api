import sqlite3

def criar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha) VALUES (?, ?)", ("admin", "1234"))

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        email TEXT,
        telefone TEXT
    )
    """)

    conexao.commit()
    conexao.close()
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco()   