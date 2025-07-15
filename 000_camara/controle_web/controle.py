from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import webbrowser

app = Flask(__name__)
VIAGENS_DB = 'viagens.db'
MANUTENCOES_DB = 'manutencoes.db'
FORMATO_DATA = "%d/%m/%Y %H:%M"


# ---------- Criação dos bancos ----------
def criar_bancos():
    conn = sqlite3.connect(VIAGENS_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS viagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT,
            destino TEXT,
            data_hora_inicio TEXT,
            data_hora_fim TEXT,
            km_inicial INTEGER,
            km_final INTEGER,
            km_deslocado INTEGER,
            tempo_viagem TEXT
        )
    ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect(MANUTENCOES_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo TEXT,
            descricao TEXT,
            valor REAL,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()


criar_bancos()


# ---------- Página Inicial ----------
@app.route('/')
def index():
    return render_template('index.html')


# ---------- VIAGENS ----------
@app.route('/viagens')
def listar_viagens():
    conn = sqlite3.connect(VIAGENS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM viagens ORDER BY id DESC")
    viagens = cursor.fetchall()
    conn.close()
    return render_template('listar_viagens.html', viagens=viagens)


@app.route('/adicionar_viagem', methods=['GET', 'POST'])
def adicionar_viagem():
    if request.method == 'POST':
        origem = request.form['origem']
        destino = request.form['destino']
        km_inicial = int(request.form['km_inicial'])
        data_inicio = datetime.strptime(request.form['data_inicio'], FORMATO_DATA)

        conn = sqlite3.connect(VIAGENS_DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO viagens (origem, destino, km_inicial, data_hora_inicio)
            VALUES (?, ?, ?, ?)
        ''', (origem, destino, km_inicial, data_inicio.strftime(FORMATO_DATA)))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_viagens'))

    return render_template('form_viagem.html')


@app.route('/encerrar_viagem/<int:viagem_id>', methods=['GET', 'POST'])
def encerrar_viagem(viagem_id):
    if request.method == 'POST':
        data_fim = datetime.strptime(request.form['data_fim'], FORMATO_DATA)
        km_final = int(request.form['km_final'])

        conn = sqlite3.connect(VIAGENS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT data_hora_inicio, km_inicial FROM viagens WHERE id = ?", (viagem_id,))
        dados = cursor.fetchone()

        if dados:
            data_inicio = datetime.strptime(dados[0], FORMATO_DATA)
            km_inicial = dados[1]

            duracao = str(data_fim - data_inicio)
            km_deslocado = km_final - km_inicial

            cursor.execute('''
                UPDATE viagens
                SET data_hora_fim = ?, km_final = ?, km_deslocado = ?, tempo_viagem = ?
                WHERE id = ?
            ''', (data_fim.strftime(FORMATO_DATA), km_final, km_deslocado, duracao, viagem_id))
            conn.commit()
        conn.close()
        return redirect(url_for('listar_viagens'))

    return render_template('form_encerrar_viagem.html', viagem_id=viagem_id)


@app.route('/relatorio_viagens')
def relatorio_viagens():
    conn = sqlite3.connect(VIAGENS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM viagens")
    viagens = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head><meta charset='utf-8'><title>Relatório de Viagens</title></head>
    <body>
    <h2>Relatório de Viagens - Câmara Municipal de Dores do Turvo</h2>
    <table border='1' cellpadding='5' cellspacing='0'>
    <tr>
        <th>ID</th><th>Origem</th><th>Destino</th><th>Início</th><th>Fim</th>
        <th>KM Inicial</th><th>KM Final</th><th>Deslocado</th><th>Duração</th>
    </tr>
    """

    for v in viagens:
        html += f"""
        <tr>
            <td>{v[0]}</td>
            <td>{v[1]}</td>
            <td>{v[2]}</td>
            <td>{v[3]}</td>
            <td>{v[4] or '-'}</td>
            <td>{v[5]}</td>
            <td>{v[6] or '-'}</td>
            <td>{v[7] or '-'}</td>
            <td>{v[8] or '-'}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open("relatorio_viagens.html", "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open("relatorio_viagens.html")
    return redirect(url_for('listar_viagens'))


# ---------- MANUTENÇÕES ----------
@app.route('/manutencoes')
def listar_manutencoes():
    conn = sqlite3.connect(MANUTENCOES_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM manutencoes ORDER BY id DESC")
    manutencoes = cursor.fetchall()
    conn.close()
    return render_template('listar_manutencoes.html', manutencoes=manutencoes)


@app.route('/adicionar_manutencao', methods=['GET', 'POST'])
def adicionar_manutencao():
    if request.method == 'POST':
        veiculo = request.form['veiculo']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = request.form['data']

        conn = sqlite3.connect(MANUTENCOES_DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO manutencoes (veiculo, descricao, valor, data)
            VALUES (?, ?, ?, ?)
        ''', (veiculo, descricao, valor, data))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_manutencoes'))

    return render_template('form_manutencao.html')


# ---------- Executar em rede local ----------
if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    print(f"\nSistema disponível em: http://{hostname}:5000/\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
