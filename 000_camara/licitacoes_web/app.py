from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3
from decimal import Decimal, InvalidOperation
from datetime import datetime

app = Flask(__name__)
DATABASE = 'licitacoes.db'

# --- Limites atualizados (Decreto nº 12.343/2024) ---
THRESHOLD_OBRAS = Decimal('125451.15')   # Art.75 I - obras e serviços de engenharia / manutenção de veículos
THRESHOLD_OUTROS = Decimal('62725.59')   # Art.75 II - outros serviços e compras
# ----------------------------------------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_objeto TEXT,
            descricao TEXT,
            valor_est REAL,
            urgencia TEXT,
            fornecedor_exclusivo INTEGER,
            servico_singular INTEGER,
            resultado TEXT,
            fundamento TEXT,
            created_at TEXT
        )
    ''')
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def parse_decimal(value_str):
    """Tenta interpretar valor em formatos comuns BR (1.234,56 ou 1234.56)"""
    if not value_str:
        return Decimal('0')
    s = value_str.strip().replace(' ', '')
    if s.count(',') == 1 and s.count('.') > 0:
        s = s.replace('.', '').replace(',', '.')
    else:
        s = s.replace(',', '.')
    try:
        return Decimal(s)
    except InvalidOperation:
        return Decimal('0')

def analisar(tipo_objeto, valor: Decimal, fornecedor_exclusivo: bool, servico_singular: bool):
    # Inexigibilidade (art.74)
    if fornecedor_exclusivo:
        return ("Inexigibilidade", "Art. 74, Lei 14.133/2021 — fornecedor exclusivo")
    if servico_singular:
        return ("Inexigibilidade", "Art. 74, Lei 14.133/2021 — serviço de natureza singular / notória especialização")

    # Dispensa por valor (art.75)
    if tipo_objeto in ('obra', 'manutencao_veiculo'):
        if valor < THRESHOLD_OBRAS:
            return ("Dispensa (Art.75, I)", f"Art. 75, I — valor inferior a R$ {THRESHOLD_OBRAS:,}")
        else:
            return ("Concorrência (obra de maior vulto)", "Lei 14.133/2021 — concorrência para obras de maior valor")
    else:
        if valor < THRESHOLD_OUTROS:
            return ("Dispensa (Art.75, II)", f"Art. 75, II — valor inferior a R$ {THRESHOLD_OUTROS:,}")
        else:
            return ("Pregão (bens/serviços comuns) — modal. preferencial", "Lei 10.520/2002 / Lei 14.133/2021 — pregão para bens/serviços comuns")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    tipo_objeto = request.form.get('tipo_objeto', '')
    descricao = request.form.get('descricao', '')
    valor_str = request.form.get('valor', '0')
    urgencia = request.form.get('urgencia', '')
    fornecedor_exclusivo = request.form.get('fornecedor_exclusivo') == 'on'
    servico_singular = request.form.get('servico_singular') == 'on'

    valor = parse_decimal(valor_str)

    resultado, fundamento = analisar(tipo_objeto, valor, fornecedor_exclusivo, servico_singular)

    db = get_db()
    db.execute('''
        INSERT INTO consultas
        (tipo_objeto, descricao, valor_est, urgencia, fornecedor_exclusivo, servico_singular, resultado, fundamento, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        tipo_objeto, descricao, float(valor), urgencia, int(fornecedor_exclusivo), int(servico_singular), resultado, fundamento, datetime.now().isoformat()
    ))
    db.commit()

    return render_template('resultado.html',
                           resultado=resultado,
                           fundamento=fundamento,
                           tipo_objeto=tipo_objeto,
                           valor=valor,
                           descricao=descricao)

@app.route('/historico')
def historico():
    db = get_db()
    cur = db.execute('SELECT * FROM consultas ORDER BY id DESC')
    rows = cur.fetchall()
    return render_template('historico.html', rows=rows)

@app.route('/detalhe/<int:id>')
def detalhe(id):
    db = get_db()
    cur = db.execute('SELECT * FROM consultas WHERE id = ?', (id,))
    row = cur.fetchone()
    if not row:
        return "Registro não encontrado", 404
    return render_template('detalhe.html', row=row)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
