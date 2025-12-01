# Controle de Impressões com SISTEMA DE USUÁRIOS COMPLETO
# Kivy + SQLite
# Melhorias incluídas:
# - Contagem automática de impressões do cliente:
#       • no dia atual
#       • na semana corrente
#       • no mês corrente
#   (ao selecionar o cliente)

import os
import sqlite3
import binascii
import hashlib
from datetime import datetime, timedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty

DB_FILE = 'impressoes.db'
SALT_BYTES = 16
PBKDF2_ITER = 100_000
FORMATO_DATA = '%d/%m/%Y %H:%M'

# ----------------- Helpers -----------------

def get_conn():
    return sqlite3.connect(DB_FILE)

def criar_tabelas_e_admin_padrao():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL,
            nome TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            contato TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS impressoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            usuario TEXT NOT NULL,
            impressora TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    ''')
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        username = 'admin'
        senha = 'admin123'
        salt = os.urandom(SALT_BYTES)
        hash_bytes = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, PBKDF2_ITER)
        cur.execute('INSERT INTO users (username, password_hash, salt, role, nome) VALUES (?, ?, ?, ?, ?)',
                    (username, binascii.hexlify(hash_bytes).decode(), binascii.hexlify(salt).decode(),
                     'admin', 'Administrador'))
        conn.commit()
    conn.close()

def gerar_hash_senha(senha, salt_hex=None):
    if salt_hex:
        salt = binascii.unhexlify(salt_hex)
    else:
        salt = os.urandom(SALT_BYTES)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, PBKDF2_ITER)
    return binascii.hexlify(hash_bytes).decode(), binascii.hexlify(salt).decode()

def verificar_senha(senha, hash_hex, salt_hex):
    novo_hash, _ = gerar_hash_senha(senha, salt_hex)
    return novo_hash == hash_hex

# ----------------- KV UI -----------------

KV = '''
ScreenManager:
    LoginScreen:
    MainScreen:
    CadastroClienteScreen:
    RegistrarImpressaoScreen:
    GerenciarUsuariosScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: 24
        spacing: 12
        Label:
            text: 'Controle de Impressões - Login'
            font_size: 22
            size_hint_y: None
            height: 40
        TextInput:
            id: username
            hint_text: 'Usuário'
            multiline: False
        TextInput:
            id: password
            hint_text: 'Senha'
            password: True
            multiline: False
        Label:
            id: lbl_msg
            text: ''
            size_hint_y: None
            height: 24
            color: 1,0,0,1
        BoxLayout:
            size_hint_y: None
            height: 48
            spacing: 8
            Button:
                text: 'Entrar'
                on_release: root.action_login(username.text, password.text)
            Button:
                text: 'Sair'
                on_release: app.stop()

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 8
        BoxLayout:
            size_hint_y: None
            height: 40
            Label:
                id: lbl_usuario
                text: 'Usuário: -'
                halign: 'left'
            Button:
                text: 'Logout'
                size_hint_x: None
                width: 100
                on_release: root.action_logout()
        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 6
            Button:
                text: 'Registrar Impressão'
                on_release: app.root.current = 'registrar'
            Button:
                text: 'Cadastrar Cliente'
                on_release: app.root.current = 'clientes'
            Button:
                text: 'Gerenciar Usuários'
                on_release: app.root.current = 'usuarios'
        Label:
            text: 'Últimos registros:'
            size_hint_y: None
            height: 28
        ScrollView:
            GridLayout:
                id: grid_registros
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 110
                row_force_default: True

<CadastroClienteScreen>:
    name: 'clientes'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 8
        Label:
            text: 'Cadastro de Cliente'
            size_hint_y: None
            height: 38
        TextInput:
            id: nome_cliente
            hint_text: 'Nome do cliente'
            multiline: False
        TextInput:
            id: contato_cliente
            hint_text: 'Contato (opcional)'
            multiline: False
        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 8
            Button:
                text: 'Salvar'
                on_release: root.salvar_cliente()
            Button:
                text: 'Voltar'
                on_release: app.root.current = 'main'
        Label:
            id: status_cliente
            text: ''

<RegistrarImpressaoScreen>:
    name: 'registrar'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 8
        Label:
            text: 'Registrar Impressão'
            size_hint_y: None
            height: 36
        Spinner:
            id: spinner_clientes
            text: 'Selecione um cliente'
            values: []
            size_hint_y: None
            height: 44
            on_text: root.cliente_selecionado(self.text)
        Label:
            id: lbl_total
            text: 'Impressões do cliente: 0'
            size_hint_y: None
            height: 26

        Label:
            id: lbl_dia
            text: 'Hoje: 0'
            size_hint_y: None
            height: 26

        Label:
            id: lbl_semana
            text: 'Semana: 0'
            size_hint_y: None
            height: 26

        Label:
            id: lbl_mes
            text: 'Mês: 0'
            size_hint_y: None
            height: 26

        TextInput:
            id: impressora
            hint_text: 'Impressora'
            multiline: False
        TextInput:
            id: quantidade
            hint_text: 'Quantidade de páginas'
            input_filter: 'int'
            multiline: False

        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 8
            Button:
                text: 'Registrar'
                on_release: root.registrar_impressao()
            Button:
                text: 'Voltar'
                on_release: app.root.current = 'main'

<GerenciarUsuariosScreen>:
    name: 'usuarios'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 8
        Label:
            text: 'Gestão de Usuários (admin)'
            size_hint_y: None
            height: 36
        BoxLayout:
            size_hint_y: None
            height: 36
            spacing: 8
            TextInput:
                id: novo_user
                hint_text: 'Novo usuário'
                multiline: False
            TextInput:
                id: nova_senha
                hint_text: 'Senha'
                password: True
                multiline: False
            Spinner:
                id: novo_role
                text: 'role'
                values: ['admin','user']
                size_hint_x: None
                width: 120
        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 8
            Button:
                text: 'Criar usuário'
                on_release: root.criar_usuario(novo_user.text, nova_senha.text, novo_role.text)
            Button:
                text: 'Voltar'
                on_release: app.root.current = 'main'
        Label:
            id: status_user
            text: ''
        ScrollView:
            GridLayout:
                id: grid_users
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 40
                row_force_default: True
'''

# ----------------- Telas -----------------

class LoginScreen(Screen):
    def action_login(self, username, password):
        if not username or not password:
            self.ids.lbl_msg.text = 'Preencha usuário e senha.'
            return
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT username, password_hash, salt, role, nome FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        conn.close()
        if not row:
            self.ids.lbl_msg.text = 'Usuário não encontrado.'
            return
        _, phash, salt, role, nome = row
        if verificar_senha(password, phash, salt):
            app = App.get_running_app()
            app.usuario_logado = username
            app.nome_usuario = nome if nome else username
            app.role = role
            self.ids.lbl_msg.text = ''
            App.get_running_app().root.current = 'main'
        else:
            self.ids.lbl_msg.text = 'Senha incorreta.'

class MainScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        self.ids.lbl_usuario.text = f'Usuário: {getattr(app, "nome_usuario", app.usuario_logado)}'

class CadastroClienteScreen(Screen):
    def salvar_cliente(self):
        nome = self.ids.nome_cliente.text.strip()
        contato = self.ids.contato_cliente.text.strip()
        if not nome:
            self.ids.status_cliente.text = 'Preencha o nome do cliente.'
            return
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO clientes (nome, contato) VALUES (?, ?)', (nome, contato if contato else None))
            conn.commit()
            self.ids.status_cliente.text = 'Cliente cadastrado.'
            self.ids.nome_cliente.text = ''
            self.ids.contato_cliente.text = ''
        except sqlite3.IntegrityError:
            self.ids.status_cliente.text = 'Cliente já existe.'
        finally:
            conn.close()

class RegistrarImpressaoScreen(Screen):
    def on_pre_enter(self):
        self.carregar_clientes_spinner()
        self.ids.impressora.text = ''
        self.ids.quantidade.text = ''
        self.ids.lbl_total.text = 'Impressões do cliente: 0'
        self.ids.lbl_dia.text = 'Hoje: 0'
        self.ids.lbl_semana.text = 'Semana: 0'
        self.ids.lbl_mes.text = 'Mês: 0'

    def carregar_clientes_spinner(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, nome FROM clientes ORDER BY nome')
        rows = cur.fetchall()
        conn.close()
        if rows:
            self.ids.spinner_clientes.values = [f"{r[0]}|{r[1]}" for r in rows]
        else:
            self.ids.spinner_clientes.values = []
        self.ids.spinner_clientes.text = 'Selecione um cliente'

    def cliente_selecionado(self, text):
        if not text or "|" not in text:
            return

        cid = int(text.split("|")[0])
        conn = get_conn()
        cur = conn.cursor()

        # Total geral
        cur.execute("SELECT SUM(quantidade) FROM impressoes WHERE cliente_id = ?", (cid,))
        total = cur.fetchone()[0] or 0
        self.ids.lbl_total.text = f"Impressões do cliente: {total}"

        hoje = datetime.now().strftime('%d/%m/%Y')

        # Dia
        cur.execute("""
            SELECT SUM(quantidade) FROM impressoes
            WHERE cliente_id = ? AND substr(data_hora, 1, 10) = ?
        """, (cid, hoje))
        dia = cur.fetchone()[0] or 0
        self.ids.lbl_dia.text = f"Hoje: {dia}"

        # Semana
        agora = datetime.now()
        ini_sem = (agora - timedelta(days=agora.weekday())).strftime('%d/%m/%Y')
        fim_sem = (agora + timedelta(days=6-agora.weekday())).strftime('%d/%m/%Y')

        cur.execute("""
            SELECT SUM(quantidade)
            FROM impressoes
            WHERE cliente_id = ?
            AND date(substr(data_hora,7,4)||'-'||substr(data_hora,4,2)||'-'||substr(data_hora,1,2))
                BETWEEN date(?) AND date(?)
        """, (cid, ini_sem, fim_sem))
        semana = cur.fetchone()[0] or 0
        self.ids.lbl_semana.text = f"Semana: {semana}"

        # Mês
        ano = agora.strftime('%Y')
        mes = agora.strftime('%m')

        cur.execute("""
            SELECT SUM(quantidade) FROM impressoes
            WHERE cliente_id = ?
            AND substr(data_hora, 4, 2) = ?
            AND substr(data_hora, 7, 4) = ?
        """, (cid, mes, ano))
        mes_count = cur.fetchone()[0] or 0
        self.ids.lbl_mes.text = f"Mês: {mes_count}"

        conn.close()

    def registrar_impressao(self):
        text = self.ids.spinner_clientes.text
        if not text or "|" not in text:
            self.ids.lbl_total.text = "Selecione um cliente válido."
            return

        cid = int(text.split("|")[0])
        impressora = self.ids.impressora.text.strip()
        quantidade = self.ids.quantidade.text.strip()

        if not impressora or not quantidade:
            self.ids.lbl_total.text = "Preencha os campos."
            return

        qtd = int(quantidade)
        if qtd <= 0:
            self.ids.lbl_total.text = "Quantidade inválida."
            return

        usuario = App.get_running_app().usuario_logado
        data_hora = datetime.now().strftime(FORMATO_DATA)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO impressoes (cliente_id, usuario, impressora, quantidade, data_hora) VALUES (?, ?, ?, ?, ?)",
            (cid, usuario, impressora, qtd, data_hora)
        )
        conn.commit()
        conn.close()

        self.cliente_selecionado(text)
        self.ids.impressora.text = ''
        self.ids.quantidade.text = ''

class GerenciarUsuariosScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        if app.role != 'admin':
            self.ids.status_user.text = 'Acesso negado.'
            return
        self.carregar_usuarios()

    def criar_usuario(self, username, senha, role):
        username = username.strip()
        senha = senha.strip()
        if not username or not senha:
            self.ids.status_user.text = 'Preencha todos os campos.'
            return

        phash, salt = gerar_hash_senha(senha)

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password_hash, salt, role, nome) VALUES (?, ?, ?, ?, ?)",
                        (username, phash, salt, role, username))
            conn.commit()
            self.ids.status_user.text = 'Usuário criado.'
            self.carregar_usuarios()
        except:
            self.ids.status_user.text = 'Erro ou usuário já existe.'
        finally:
            conn.close()

    def carregar_usuarios(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM users ORDER BY username")
        rows = cur.fetchall()
        conn.close()
        grid = self.ids.grid_users
        grid.clear_widgets()
        from kivy.uix.label import Label
        for r in rows:
            grid.add_widget(Label(text=f'{r[0]} — {r[1]}', size_hint_y=None, height=36))

# ----------------- App -----------------

class ControleImpressoesApp(App):
    usuario_logado = None
    nome_usuario = None
    role = None

    def build(self):
        criar_tabelas_e_admin_padrao()
        return Builder.load_string(KV)

# ----------------- Run -----------------

if __name__ == '__main__':
    ControleImpressoesApp().run()
