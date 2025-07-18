from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF
import os

app = Flask(__name__)
DB = 'ouvidoria.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS manifestacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        datahora TEXT NOT NULL,
        meio TEXT NOT NULL,
        prazo TEXT NOT NULL,
        status TEXT NOT NULL,
        resposta TEXT,
        servidor TEXT,
        dataresposta TEXT
    )''')
    conn.commit()
    conn.close()

def calcular_prazo_uteis(dias_uteis):
    data = datetime.now()
    adicionados = 0
    while adicionados < dias_uteis:
        data += timedelta(days=1)
        if data.weekday() < 5:  # Segunda a sexta
            adicionados += 1
    return data.strftime('%d/%m/%Y')

def calcular_prazo_corridos(dias):
    data = datetime.now() + timedelta(days=dias)
    return data.strftime('%d/%m/%Y')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    tipo = request.form['tipo']
    descricao = request.form['descricao']
    meio = request.form['meio']
    dias = int(request.form['dias'] or 0)
    prazo_tipo = request.form.get('prazo_tipo', 'corridos')  # novo campo
    
    if prazo_tipo == 'uteis':
        prazo = calcular_prazo_uteis(dias)
    else:
        prazo = calcular_prazo_corridos(dias)

    datahora = datetime.now().strftime('%d/%m/%Y %H:%M')

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO manifestacoes
        (nome, tipo, descricao, datahora, meio, prazo, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (nome, tipo, descricao, datahora, meio, prazo, 'Pendente'))
    conn.commit()
    conn.close()
    return redirect(url_for('listar'))

@app.route('/listar')
def listar():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM manifestacoes ORDER BY id DESC')
    regs = c.fetchall()
    conn.close()
    return render_template('listar.html', regs=regs)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        status = request.form['status']
        resposta = request.form['resposta']
        servidor = request.form['servidor']
        dataresposta = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.execute('''
            UPDATE manifestacoes
            SET status=?, resposta=?, servidor=?, dataresposta=?
            WHERE id=?''',
            (status, resposta, servidor, dataresposta, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))

    c.execute('SELECT * FROM manifestacoes WHERE id=?', (id,))
    m = c.fetchone()
    conn.close()
    return render_template('editar.html', m=m)

@app.route('/pdf')
def gerar_pdf():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM manifestacoes ORDER BY id DESC')
    regs = c.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Relatório - Ouvidoria", ln=True, align='C')
    pdf.ln(10)

    for r in regs:
        pdf.multi_cell(0, 10,
            f"ID: {r[0]}\nNome: {r[1]}\nTipo: {r[2]}\nDescrição: {r[3]}\n"
            f"Data: {r[4]}\nMeio: {r[5]}\nPrazo: {r[6]}\nStatus: {r[7]}\n"
            f"Resposta: {r[8] or '---'}\nServidor: {r[9] or '---'}\n"
            f"Data Resposta: {r[10] or '---'}\n"
        )
        pdf.ln(5)

    pdf.output('relatorio_ouvidoria.pdf')
    return redirect(url_for('listar'))

@app.route('/relatorio')
def relatorio_html():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM manifestacoes ORDER BY id DESC')
    regs = c.fetchall()
    conn.close()
    return render_template('relatorio.html', regs=regs)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
