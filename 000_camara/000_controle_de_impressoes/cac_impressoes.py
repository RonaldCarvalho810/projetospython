# cac_impressoes.py
# Controle de Impressões com SISTEMA DE USUÁRIOS COMPLETO
# Compatível com PyInstaller --windowed --onefile
# DB fica no mesmo diretório do EXE
# Proteção stdout/stderr + logging em arquivo
# Correção: preencher Spinner do login com schedule (evita KeyError)

import sys
import os
import sqlite3
import binascii
import hashlib
from datetime import datetime, timedelta

# --- Proteção para quando rodar com PyInstaller --windowed (sem console) ---
class _DevNull:
    def write(self, _): pass
    def flush(self): pass

if not hasattr(sys, "stdout") or sys.stdout is None:
    sys.stdout = _DevNull()
if not hasattr(sys, "stderr") or sys.stderr is None:
    sys.stderr = _DevNull()

# --- logging para arquivo ---
import logging
LOG_FILE = "app.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logging.info("Aplicação iniciando...")

# agora importa Kivy (depois de proteger stdout/stderr)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# ---------------- configuração do caminho do banco ----------------
if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(base_dir, "impressoes.db")
SALT_BYTES = 16
PBKDF2_ITER = 100_000
FORMATO_DATA = "%d/%m/%Y %H:%M"

# ----------------- Helpers -----------------

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        logging.exception("PRAGMA WAL falhou")
    return conn

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

    try:
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            username = "admin"
            senha = "admin123"
            salt = os.urandom(SALT_BYTES)
            hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, PBKDF2_ITER)
            cur.execute(
                "INSERT INTO users (username, password_hash, salt, role, nome) VALUES (?, ?, ?, ?, ?)",
                (username, binascii.hexlify(hash_bytes).decode(), binascii.hexlify(salt).decode(), "admin", "Administrador"),
            )
            conn.commit()
            logging.info("Usuário admin criado (padrão).")
    except Exception:
        logging.exception("Erro ao criar admin padrão")
    finally:
        conn.close()

def gerar_hash_senha(senha, salt_hex=None):
    if salt_hex:
        salt = binascii.unhexlify(salt_hex)
    else:
        salt = os.urandom(SALT_BYTES)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, PBKDF2_ITER)
    return binascii.hexlify(hash_bytes).decode(), binascii.hexlify(salt).decode()

def verificar_senha(senha, hash_hex, salt_hex):
    novo_hash, _ = gerar_hash_senha(senha, salt_hex)
    return novo_hash == hash_hex

# ----------------- KV UI -----------------
KV = r'''
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

        Spinner:
            id: combo_users
            text: 'Selecione o usuário'
            values: []
            size_hint_y: None
            height: 44

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
                on_release: root.action_login(combo_users.text, password.text)
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
    def on_pre_enter(self, *args):
        # schedule to run after widgets are built to avoid KeyError on ids
        Clock.schedule_once(self._carregar_usuarios_safe, 0)

    def _carregar_usuarios_safe(self, dt):
        self.carregar_usuarios()

    def carregar_usuarios(self):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT username FROM users ORDER BY username")
            rows = cur.fetchall()
            conn.close()
            users = [r[0] for r in rows] if rows else []
        except Exception:
            logging.exception("Erro ao carregar usuários")
            users = []

        spinner = self.ids.get("combo_users")
        if spinner:
            try:
                spinner.values = users
                spinner.text = 'Selecione o usuário' if users else 'Nenhum usuário'
            except Exception:
                logging.exception("Erro ao preencher spinner combo_users")
        else:
            logging.warning("combo_users não encontrado em ids do LoginScreen")

    def action_login(self, username, password):
        if not username or username == "Selecione o usuário" or username == "Nenhum usuário":
            self.ids.lbl_msg.text = "Escolha um usuário."
            return

        if not password:
            self.ids.lbl_msg.text = 'Digite a senha.'
            return

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('SELECT username, password_hash, salt, role, nome FROM users WHERE username = ?', (username,))
            row = cur.fetchone()
            conn.close()
        except Exception:
            logging.exception("Erro ao consultar usuário")
            self.ids.lbl_msg.text = 'Erro no banco.'
            return

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
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.ids.lbl_usuario.text = f'Usuário: {getattr(app, "nome_usuario", app.usuario_logado)}'
        self.carregar_ultimos()

    def action_logout(self):
        App.get_running_app().usuario_logado = None
        App.get_running_app().root.current = "login"

    def carregar_ultimos(self):
        grid = self.ids.grid_registros
        grid.clear_widgets()
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('''
                SELECT i.id, c.nome, i.usuario, i.impressora, i.quantidade, i.data_hora
                FROM impressoes i
                JOIN clientes c ON i.cliente_id = c.id
                ORDER BY i.id DESC
                LIMIT 50
            ''')
            rows = cur.fetchall()
            conn.close()
        except Exception:
            logging.exception("Erro ao carregar últimos registros")
            from kivy.uix.label import Label
            grid.add_widget(Label(text='Erro ao carregar registros.', size_hint_y=None, height=40))
            return

        if not rows:
            from kivy.uix.label import Label
            grid.add_widget(Label(text='Nenhum registro ainda.', size_hint_y=None, height=40))
            return

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        for r in rows:
            texto = f"ID: {r[0]}\nCliente: {r[1]}\nUsuário: {r[2]}\nImpressora: {r[3]}\nQuantidade: {r[4]}\nData: {r[5]}"
            b = BoxLayout(orientation='vertical', size_hint_y=None, height=110, padding=6)
            b.add_widget(Label(text=texto))
            grid.add_widget(b)

class CadastroClienteScreen(Screen):
    def salvar_cliente(self):
        nome = self.ids.nome_cliente.text.strip()
        contato = self.ids.contato_cliente.text.strip()
        if not nome:
            self.ids.status_cliente.text = 'Preencha o nome do cliente.'
            return
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('INSERT INTO clientes (nome, contato) VALUES (?, ?)', (nome, contato or None))
            conn.commit()
            conn.close()
            self.ids.status_cliente.text = 'Cliente cadastrado.'
            self.ids.nome_cliente.text = ''
            self.ids.contato_cliente.text = ''
        except sqlite3.IntegrityError:
            self.ids.status_cliente.text = 'Cliente já existe.'
        except Exception:
            logging.exception("Erro ao salvar cliente")
            self.ids.status_cliente.text = 'Erro ao salvar cliente.'

class RegistrarImpressaoScreen(Screen):
    def on_pre_enter(self, *args):
        # preencher spinner de clientes quando a tela for exibida
        Clock.schedule_once(lambda dt: self.carregar_clientes_spinner(), 0)
        self.ids.impressora.text = ''
        self.ids.quantidade.text = ''
        self.ids.lbl_total.text = 'Impressões do cliente: 0'
        self.ids.lbl_dia.text = 'Hoje: 0'
        self.ids.lbl_semana.text = 'Semana: 0'
        self.ids.lbl_mes.text = 'Mês: 0'

    def carregar_clientes_spinner(self):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('SELECT id, nome FROM clientes ORDER BY nome')
            rows = cur.fetchall()
            conn.close()
        except Exception:
            logging.exception("Erro ao carregar clientes")
            rows = []

        spinner = self.ids.get("spinner_clientes")
        if spinner:
            try:
                spinner.values = [f"{r[0]}|{r[1]}" for r in rows] if rows else []
                spinner.text = 'Selecione um cliente' if rows else 'Nenhum cliente'
            except Exception:
                logging.exception("Erro ao preencher spinner_clientes")
        else:
            logging.warning("spinner_clientes não encontrado em ids de RegistrarImpressaoScreen")

    def cliente_selecionado(self, text):
        if "|" not in text:
            self.ids.lbl_total.text = 'Impressões do cliente: 0'
            self.ids.lbl_dia.text = 'Hoje: 0'
            self.ids.lbl_semana.text = 'Semana: 0'
            self.ids.lbl_mes.text = 'Mês: 0'
            return

        cid = int(text.split("|")[0])
        try:
            conn = get_conn()
            cur = conn.cursor()
        except Exception:
            logging.exception("Erro DB")
            return

        # Total geral
        cur.execute("SELECT SUM(quantidade) FROM impressoes WHERE cliente_id = ?", (cid,))
        total = cur.fetchone()[0] or 0
        self.ids.lbl_total.text = f"Impressões do cliente: {total}"

        agora = datetime.now()

        # Dia
        hoje_sql = agora.date().isoformat()
        cur.execute("""
            SELECT SUM(quantidade)
            FROM impressoes
            WHERE cliente_id = ?
              AND date(substr(data_hora,7,4) || '-' || substr(data_hora,4,2) || '-' || substr(data_hora,1,2)) = date(?)
        """, (cid, hoje_sql))
        dia = cur.fetchone()[0] or 0
        self.ids.lbl_dia.text = f"Hoje: {dia}"

        # Semana (segunda -> domingo)
        inicio_sem = (agora - timedelta(days=agora.weekday())).date().isoformat()
        fim_sem = (agora + timedelta(days=(6 - agora.weekday()))).date().isoformat()
        cur.execute("""
            SELECT SUM(quantidade)
            FROM impressoes
            WHERE cliente_id = ?
              AND date(substr(data_hora,7,4) || '-' || substr(data_hora,4,2) || '-' || substr(data_hora,1,2))
                  BETWEEN date(?) AND date(?)
        """, (cid, inicio_sem, fim_sem))
        semana = cur.fetchone()[0] or 0
        self.ids.lbl_semana.text = f"Semana: {semana}"

        # Mês
        mes_atual = agora.strftime('%m')
        ano_atual = agora.strftime('%Y')
        cur.execute("""
            SELECT SUM(quantidade)
            FROM impressoes
            WHERE cliente_id = ?
              AND substr(data_hora,4,2) = ? AND substr(data_hora,7,4) = ?
        """, (cid, mes_atual, ano_atual))
        mes_count = cur.fetchone()[0] or 0
        self.ids.lbl_mes.text = f"Mês: {mes_count}"

        conn.close()

    def registrar_impressao(self):
        text = self.ids.spinner_clientes.text
        if "|" not in text:
            self.ids.lbl_total.text = "Selecione um cliente válido."
            return

        cid = int(text.split("|")[0])
        impressora = self.ids.impressora.text.strip()
        quantidade = self.ids.quantidade.text.strip()

        if not impressora or not quantidade:
            self.ids.lbl_total.text = "Preencha os campos."
            return

        try:
            qtd = int(quantidade)
            if qtd <= 0:
                raise ValueError()
        except Exception:
            self.ids.lbl_total.text = "Quantidade inválida."
            return

        usuario = App.get_running_app().usuario_logado or "desconhecido"
        data_hora = datetime.now().strftime(FORMATO_DATA)

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO impressoes (cliente_id, usuario, impressora, quantidade, data_hora)
                VALUES (?, ?, ?, ?, ?)
            """, (cid, usuario, impressora, qtd, data_hora))
            conn.commit()
            conn.close()
        except Exception:
            logging.exception("Erro ao inserir impressão")
            self.ids.lbl_total.text = "Erro ao gravar."
            return

        # Atualiza contagens
        Clock.schedule_once(lambda dt: self.cliente_selecionado(self.ids.spinner_clientes.text), 0)
        self.ids.impressora.text = ''
        self.ids.quantidade.text = ''

class GerenciarUsuariosScreen(Screen):
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if app.role != "admin":
            # Se não for admin, mostramos mensagem simples
            try:
                self.ids.status_user.text = "Acesso negado."
            except Exception:
                pass
            return
        Clock.schedule_once(lambda dt: self.carregar_usuarios(), 0)

    def criar_usuario(self, username, senha, role):
        username = username.strip()
        senha = senha.strip()
        if not username or not senha:
            try:
                self.ids.status_user.text = "Preencha todos os campos."
            except Exception:
                pass
            return

        phash, salt = gerar_hash_senha(senha)
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (username, password_hash, salt, role, nome)
                VALUES (?, ?, ?, ?, ?)
            """, (username, phash, salt, role, username))
            conn.commit()
            try:
                self.ids.status_user.text = "Usuário criado."
            except Exception:
                pass
            self.carregar_usuarios()
        except Exception:
            logging.exception("Erro ao criar usuário")
            try:
                self.ids.status_user.text = "Erro ou usuário já existe."
            except Exception:
                pass
        finally:
            conn.close()

    def carregar_usuarios(self):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT username, role FROM users ORDER BY username")
            rows = cur.fetchall()
            conn.close()
        except Exception:
            logging.exception("Erro ao buscar usuários")
            rows = []

        grid = self.ids.get("grid_users")
        if grid is None:
            logging.warning("grid_users não encontrado")
            return
        grid.clear_widgets()
        from kivy.uix.label import Label
        for r in rows:
            grid.add_widget(Label(text=f"{r[0]} — {r[1]}", size_hint_y=None, height=36))

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
    logging.info("Aplicação pronta para rodar. DB em: %s", DB_FILE)
    ControleImpressoesApp().run()
