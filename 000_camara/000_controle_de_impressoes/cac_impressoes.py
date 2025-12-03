# cac_impressoes.py
# Sistema de Controle de Impressões (único arquivo, KV embutido)
# Requer: kivy, python 3.8+
# Salve este arquivo na pasta onde ficará o EXE; o banco (impressoes.db) será criado ali.

import os
import sys
import sqlite3
import binascii
import hashlib
import logging
from datetime import datetime, timedelta, date

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

# ---------- Window (opcional) ----------
Window.size = (800, 600)

# ---------- paths & logging ----------
BASE_DIR = os.path.dirname(getattr(sys, '_MEIPASS', os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "impressoes.db")
LOG_FILE = os.path.join(BASE_DIR, "app.log")

# Keep a reference to any fallback devnull file to avoid GC closing it.
_DEVNULL_FH = None

# configuração de logging robusta para .exe sem console
def setup_logging():
    global _DEVNULL_FH
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # remover handlers existentes (evita duplicação em reloads) e fechar streams
    for h in list(logger.handlers):
        try:
            logger.removeHandler(h)
        except Exception:
            pass
        try:
            h.close()
        except Exception:
            pass

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # Certificar que base dir existe (embora já exista normalmente)
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
    except Exception:
        # se não conseguir criar, seguimos (fallback tratará)
        pass

    # 1) tentar abrir arquivo de log
    try:
        # Garante que arquivo possa ser criado (dir ok)
        fh = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.propagate = False
        logger.info("Aplicativo iniciando (arquivo de log).")
        return
    except Exception:
        # se falhar, seguir para fallback
        try:
            # se falhou por permissão no arquivo, tentamos criar diretório 'logs' ao lado
            logs_dir = os.path.join(BASE_DIR, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            alt_log = os.path.join(logs_dir, "app.log")
            fh = logging.FileHandler(alt_log, mode='a', encoding='utf-8')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.propagate = False
            logger.info("Aplicativo iniciando (arquivo de log alternativo).")
            return
        except Exception:
            pass

    # 2) tentar escrever em stderr válido (sys.__stderr__ costuma existir mesmo em exe GUI)
    stream_obj = None
    try:
        # preferir sys.__stderr__ quando existe e não está fechado
        cand = getattr(sys, '__stderr__', None) or getattr(sys, 'stderr', None)
        if cand and hasattr(cand, 'write') and not getattr(cand, 'closed', False):
            stream_obj = cand
    except Exception:
        stream_obj = None

    # 2b) se stderr inválido, abrir devnull como fallback (garante um stream com write)
    try:
        if stream_obj is None:
            # abrir devnull em modo texto (mantemos referência global para evitar GC fechar)
            try:
                _DEVNULL_FH = open(os.devnull, 'w', encoding='utf-8', errors='ignore')
                stream_obj = _DEVNULL_FH
            except Exception:
                _DEVNULL_FH = None
                stream_obj = None

        if stream_obj is not None:
            sh = logging.StreamHandler(stream_obj)
            sh.setFormatter(formatter)
            logger.addHandler(sh)
            logger.propagate = False
            logger.info("Aplicativo iniciando (stderr/devnull).")
            # NOTA: não fechamos _DEVNULL_FH; mantemos referência global.
            return
    except Exception:
        pass

    # 3) último recurso: NullHandler (evita exceções em emit)
    try:
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
    except Exception:
        # nada a fazer - garantir que não exploda
        pass

# inicializa logging
setup_logging()

# ---------- security params ----------
SALT_BYTES = 16
PBKDF2_ITER = 100_000
FORMATO_DATA = "%Y-%m-%d %H:%M"  # ISO-like for SQLite-friendly handling

# ---------- Database helpers ----------
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass
    return conn

def criar_tabelas_e_admin_padrao():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS operadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            nome TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS impressoras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS impressoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operador TEXT NOT NULL,
            usuario TEXT NOT NULL,
            impressora TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()

    # criar operador admin padrão se não existir
    cur.execute("SELECT COUNT(*) FROM operadores")
    if cur.fetchone()[0] == 0:
        username = "admin"
        senha = "admin123"
        salt = os.urandom(SALT_BYTES)
        hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, PBKDF2_ITER)
        cur.execute('INSERT INTO operadores (username, password_hash, salt, nome) VALUES (?, ?, ?, ?)',
                    (username, binascii.hexlify(hash_bytes).decode(), binascii.hexlify(salt).decode(), "Administrador"))
        conn.commit()
        logging.info("Operador admin criado (padrão)")
    conn.close()

# ---------- password helpers ----------
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

# ---------- KV (embutido) ----------
KV = r'''
#:import NoTransition kivy.uix.screenmanager.NoTransition

<SmButton@Button>:
    size_hint_y: None
    height: 44
    font_size: '16sp'

ScreenManager:
    transition: NoTransition()
    LoginScreen:
    HomeScreen:
    CadOperadorScreen:
    CadUsuarioScreen:
    CadImpressoraScreen:
    RegistrarScreen:
    RelatorioScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: 24
        spacing: 12

        Label:
            text: 'Controle de Impressões — Login'
            font_size: '22sp'
            size_hint_y: None
            height: 44

        Spinner:
            id: spinner_operadores
            text: 'Selecione o operador'
            values: []
            size_hint_y: None
            height: 40

        TextInput:
            id: input_senha
            hint_text: 'Senha'
            password: True
            multiline: False
            size_hint_y: None
            height: 36
            font_size: '14sp'

        Label:
            id: lbl_info
            text: ''
            color: 1,0,0,1
            size_hint_y: None
            height: 20

        BoxLayout:
            size_hint_y: None
            height: 46
            spacing: 8
            SmButton:
                text: 'Entrar'
                on_release: root.action_login(spinner_operadores.text, input_senha.text)
            SmButton:
                text: 'Sair'
                on_release: app.stop()

<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        padding: 16
        spacing: 12

        Label:
            id: lbl_operador
            text: 'Operador: -'
            font_size: '18sp'
            size_hint_y: None
            height: 36

        GridLayout:
            cols: 2
            spacing: 10
            size_hint_y: None
            height: self.minimum_height

            SmButton:
                text: 'Registrar Impressão'
                on_release:
                    app.preencher_registro()
                    app.root.current = 'registrar'

            SmButton:
                text: 'Cadastro de Operador'
                on_release: app.root.current = 'cad_operador'

            SmButton:
                text: 'Cadastro de Usuário (cliente)'
                on_release: app.root.current = 'cad_usuario'

            SmButton:
                text: 'Cadastro de Impressora'
                on_release: app.root.current = 'cad_impressora'

            SmButton:
                text: 'Relatório por Impressora'
                on_release:
                    app.root.get_screen('relatorio').gerar_relatorio()
                    app.root.current = 'relatorio'

            SmButton:
                text: 'Logout'
                on_release:
                    app.usuario_logado = None
                    app.nome_usuario = None
                    app.root.current = 'login'

<CadOperadorScreen>:
    name: 'cad_operador'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 10

        Label:
            text: 'Cadastro de Operador'
            size_hint_y: None
            height: 36
            font_size: '18sp'

        TextInput:
            id: novo_username
            hint_text: 'Username (login)'
            multiline: False
            size_hint_y: None
            height: 40

        TextInput:
            id: novo_nome
            hint_text: 'Nome (opcional)'
            multiline: False
            size_hint_y: None
            height: 40

        TextInput:
            id: novo_senha
            hint_text: 'Senha'
            password: True
            multiline: False
            size_hint_y: None
            height: 40
            font_size: '14sp'

        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 8
            SmButton:
                text: 'Salvar'
                on_release: root.salvar_operador()
            SmButton:
                text: 'Voltar'
                on_release: app.root.current = 'home'

        Label:
            id: msg_op
            text: ''
            size_hint_y: None
            height: 24
            color: 0,0.6,0,1

        ScrollView:
            size_hint: 1, 1
            GridLayout:
                id: grid_operadores
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 28
                row_force_default: True

<CadUsuarioScreen>:
    name: 'cad_usuario'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 10

        Label:
            text: 'Cadastro de Usuário (cliente)'
            size_hint_y: None
            height: 36
            font_size: '18sp'

        TextInput:
            id: novo_usuario
            hint_text: 'Nome do cliente'
            multiline: False
            size_hint_y: None
            height: 40

        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 8
            SmButton:
                text: 'Salvar'
                on_release: root.salvar_usuario()
            SmButton:
                text: 'Voltar'
                on_release: app.root.current = 'home'

        ScrollView:
            GridLayout:
                id: grid_usuarios
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 28
                row_force_default: True

<CadImpressoraScreen>:
    name: 'cad_impressora'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 10

        Label:
            text: 'Cadastro de Impressora'
            size_hint_y: None
            height: 36
            font_size: '18sp'

        TextInput:
            id: nova_impressora
            hint_text: 'Nome da impressora'
            multiline: False
            size_hint_y: None
            height: 40

        BoxLayout:
            size_hint_y: None
            height: 44
            spacing: 8
            SmButton:
                text: 'Salvar'
                on_release: root.salvar_impressora()
            SmButton:
                text: 'Voltar'
                on_release: app.root.current = 'home'

        ScrollView:
            GridLayout:
                id: grid_impressoras
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 28
                row_force_default: True

<RegistrarScreen>:
    name: 'registrar'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 8

        Label:
            text: 'Registrar Impressão'
            size_hint_y: None
            height: 36
            font_size: '18sp'

        Label:
            id: lbl_oper_reg
            text: 'Operador: -'
            size_hint_y: None
            height: 24

        Spinner:
            id: spinner_usuario
            text: 'Selecione o usuário'
            values: []
            size_hint_y: None
            height: 40
            on_text: root.usuario_selecionado(self.text)

        Label:
            id: lbl_total_geral
            text: 'Total (cliente): 0'
            size_hint_y: None
            height: 22

        Label:
            id: lbl_hoje
            text: 'Hoje: 0'
            size_hint_y: None
            height: 20

        Label:
            id: lbl_semana
            text: 'Semana: 0'
            size_hint_y: None
            height: 20

        Label:
            id: lbl_mes
            text: 'Mês: 0'
            size_hint_y: None
            height: 20

        Spinner:
            id: spinner_impressora
            text: 'Selecione a impressora'
            values: []
            size_hint_y: None
            height: 40

        TextInput:
            id: input_qtd
            hint_text: 'Quantidade de páginas'
            input_filter: 'int'
            multiline: False
            size_hint_y: None
            height: 40

        BoxLayout:
            size_hint_y: None
            height: 46
            spacing: 8
            SmButton:
                text: 'Registrar'
                on_release: root.registrar_impressao()
            SmButton:
                text: 'Voltar'
                on_release: app.root.current = 'home'

<RelatorioScreen>:
    name: 'relatorio'
    BoxLayout:
        orientation: 'vertical'
        padding: 12
        spacing: 8

        Label:
            text: 'Relatório por Impressora'
            size_hint_y: None
            height: 36
            font_size: '18sp'

        SmButton:
            text: 'Gerar Relatório (total / mensal / anual)'
            on_release: root.gerar_relatorio()

        ScrollView:
            Label:
                id: txt_relatorio
                text: ''
                markup: True
                size_hint_y: None
                height: self.texture_size[1]

        SmButton:
            text: 'Voltar'
            on_release: app.root.current = 'home'
'''

# ---------- Screens (Python) ----------
class LoginScreen(Screen):
    def on_pre_enter(self, *args):
        # Preencher spinner de operadores (agendar no próximo frame para garantir widgets prontos)
        Clock.schedule_once(lambda dt: self.preencher_operadores(), 0)

    def preencher_operadores(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT username FROM operadores ORDER BY username")
            rows = cur.fetchall()
            conn.close()
            nomes = [r[0] for r in rows]
        except Exception:
            logging.exception("Erro ao carregar operadores")
            nomes = []
        spinner = self.ids.get("spinner_operadores")
        if spinner:
            spinner.values = nomes
            spinner.text = nomes[0] if nomes else "Nenhum operador"

    def action_login(self, username, senha):
        if not username or username in ("", "Selecione o operador", "Nenhum operador"):
            self.ids.lbl_info.text = "Selecione um operador."
            return
        if not senha:
            self.ids.lbl_info.text = "Digite a senha."
            return
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT password_hash, salt, nome FROM operadores WHERE username = ?", (username,))
            row = cur.fetchone()
            conn.close()
        except Exception:
            logging.exception("Erro ao consultar operador")
            self.ids.lbl_info.text = "Erro de banco."
            return
        if not row:
            self.ids.lbl_info.text = "Operador não encontrado."
            return
        phash, salt, nome = row
        if verificar_senha(senha, phash, salt):
            app = App.get_running_app()
            app.usuario_logado = username
            app.nome_usuario = nome if nome else username
            # Atualizar label e trocar tela
            home = app.root.get_screen("home")
            home.ids.lbl_operador.text = f"Operador: {app.nome_usuario}"
            app.root.current = "home"
            self.ids.lbl_info.text = ""
        else:
            self.ids.lbl_info.text = "Senha incorreta."

class HomeScreen(Screen):
    pass

class CadOperadorScreen(Screen):
    def on_pre_enter(self, *a):
        Clock.schedule_once(lambda dt: self.carregar_operadores(), 0)

    def salvar_operador(self):
        username = self.ids.novo_username.text.strip()
        nome = self.ids.novo_nome.text.strip()
        senha = self.ids.novo_senha.text.strip()
        if not username or not senha:
            self.ids.msg_op.text = "Preencha usuário e senha."
            return
        try:
            phash, salt = gerar_hash_senha(senha)
            conn = get_conn(); cur = conn.cursor()
            cur.execute("INSERT INTO operadores (username, password_hash, salt, nome) VALUES (?, ?, ?, ?)",
                        (username, phash, salt, nome if nome else username))
            conn.commit(); conn.close()
            self.ids.novo_username.text = ""; self.ids.novo_nome.text = ""; self.ids.novo_senha.text = ""
            self.ids.msg_op.text = "Operador salvo."
            logging.info("Operador criado: %s", username)
            self.carregar_operadores()
        except sqlite3.IntegrityError:
            self.ids.msg_op.text = "Username já existe."
        except Exception:
            logging.exception("Erro salvar operador")
            self.ids.msg_op.text = "Erro ao salvar."

    def carregar_operadores(self):
        grid = self.ids.get("grid_operadores")
        grid.clear_widgets()
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT username, nome FROM operadores ORDER BY username")
            rows = cur.fetchall(); conn.close()
        except Exception:
            logging.exception("Erro carregar operadores")
            rows = []
        from kivy.uix.label import Label
        for r in rows:
            grid.add_widget(Label(text=f"{r[0]} — {r[1]}", size_hint_y=None, height=28))

class CadUsuarioScreen(Screen):
    def on_pre_enter(self, *a):
        Clock.schedule_once(lambda dt: self.carregar_usuarios(), 0)

    def salvar_usuario(self):
        nome = self.ids.novo_usuario.text.strip()
        if not nome:
            return
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
            conn.commit(); conn.close()
            self.ids.novo_usuario.text = ""
            logging.info("Usuário cadastrado: %s", nome)
            self.carregar_usuarios()
        except sqlite3.IntegrityError:
            logging.info("Usuário já existe: %s", nome)
        except Exception:
            logging.exception("Erro salvar usuário")

    def carregar_usuarios(self):
        grid = self.ids.get("grid_usuarios")
        grid.clear_widgets()
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT nome FROM usuarios ORDER BY nome")
            rows = cur.fetchall(); conn.close()
        except Exception:
            logging.exception("Erro carregar usuarios")
            rows = []
        from kivy.uix.label import Label
        for r in rows:
            grid.add_widget(Label(text=r[0], size_hint_y=None, height=28))

class CadImpressoraScreen(Screen):
    def on_pre_enter(self, *a):
        Clock.schedule_once(lambda dt: self.carregar_impressoras(), 0)

    def salvar_impressora(self):
        nome = self.ids.nova_impressora.text.strip()
        if not nome:
            return
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("INSERT INTO impressoras (nome) VALUES (?)", (nome,))
            conn.commit(); conn.close()
            self.ids.nova_impressora.text = ""
            logging.info("Impressora cadastrada: %s", nome)
            self.carregar_impressoras()
        except sqlite3.IntegrityError:
            logging.info("Impressora já existe: %s", nome)
        except Exception:
            logging.exception("Erro salvar impressora")

    def carregar_impressoras(self):
        grid = self.ids.get("grid_impressoras")
        grid.clear_widgets()
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT nome FROM impressoras ORDER BY nome")
            rows = cur.fetchall(); conn.close()
        except Exception:
            logging.exception("Erro carregar impressoras")
            rows = []
        from kivy.uix.label import Label
        for r in rows:
            grid.add_widget(Label(text=r[0], size_hint_y=None, height=28))

class RegistrarScreen(Screen):
    def on_pre_enter(self, *a):
        # preencher spinners
        Clock.schedule_once(lambda dt: self.preencher_spinners(), 0)
        self.ids.lbl_total_geral.text = "Total (cliente): 0"
        self.ids.lbl_hoje.text = "Hoje: 0"
        self.ids.lbl_semana.text = "Semana: 0"
        self.ids.lbl_mes.text = "Mês: 0"
        # set operator label
        app = App.get_running_app()
        self.ids.lbl_oper_reg.text = f"Operador: {app.nome_usuario if app.nome_usuario else app.usuario_logado}"

    def preencher_spinners(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT nome FROM usuarios ORDER BY nome"); usuarios = [r[0] for r in cur.fetchall()]
            cur.execute("SELECT nome FROM impressoras ORDER BY nome"); impressoras = [r[0] for r in cur.fetchall()]
            conn.close()
        except Exception:
            logging.exception("Erro preencher spinners")
            usuarios = []; impressoras = []
        sp_u = self.ids.get("spinner_usuario"); sp_i = self.ids.get("spinner_impressora")
        if sp_u:
            sp_u.values = usuarios
            sp_u.text = usuarios[0] if usuarios else "Selecione o usuário"
        if sp_i:
            sp_i.values = impressoras
            sp_i.text = impressoras[0] if impressoras else "Selecione a impressora"

    def usuario_selecionado(self, text):
        if not text or text in ("", "Selecione o usuário"):
            self.ids.lbl_total_geral.text = "Total (cliente): 0"
            self.ids.lbl_hoje.text = "Hoje: 0"
            self.ids.lbl_semana.text = "Semana: 0"
            self.ids.lbl_mes.text = "Mês: 0"
            return
        cliente = text
        try:
            conn = get_conn(); cur = conn.cursor()
            # total
            cur.execute("SELECT SUM(quantidade) FROM impressoes WHERE usuario = ?", (cliente,))
            total = cur.fetchone()[0] or 0
            # hoje (compare date part)
            hoje = date.today().isoformat()
            cur.execute("SELECT SUM(quantidade) FROM impressoes WHERE usuario = ? AND date(substr(data_hora,1,10)) = date(?)", (cliente, hoje))
            dia = cur.fetchone()[0] or 0
            # semana (segunda -> domingo)
            agora = date.today()
            inicio_sem = (agora - timedelta(days=agora.weekday())).isoformat()
            fim_sem = (agora + timedelta(days=(6 - agora.weekday()))).isoformat()
            cur.execute("SELECT SUM(quantidade) FROM impressoes WHERE usuario = ? AND date(substr(data_hora,1,10)) BETWEEN date(?) AND date(?)", (cliente, inicio_sem, fim_sem))
            semana = cur.fetchone()[0] or 0
            # mês
            mes = agora.strftime("%m"); ano = agora.strftime("%Y")
            # data_hora format YYYY-MM-DD HH:MM -> substr positions: year=1-4, month=6-7
            cur.execute("SELECT SUM(quantidade) FROM impressoes WHERE usuario = ? AND substr(data_hora,6,2) = ? AND substr(data_hora,1,4) = ?", (cliente, mes, ano))
            mes_count = cur.fetchone()[0] or 0
            conn.close()
            self.ids.lbl_total_geral.text = f"Total (cliente): {total}"
            self.ids.lbl_hoje.text = f"Hoje: {dia}"
            self.ids.lbl_semana.text = f"Semana: {semana}"
            self.ids.lbl_mes.text = f"Mês: {mes_count}"
        except Exception:
            logging.exception("Erro calcular totais")
            self.ids.lbl_total_geral.text = "Total (cliente): 0"

    def registrar_impressao(self):
        operador = App.get_running_app().usuario_logado
        usuario = self.ids.spinner_usuario.text
        impressora = self.ids.spinner_impressora.text
        qtd_text = self.ids.input_qtd.text.strip()
        if not operador or not usuario or not impressora or not qtd_text.isdigit():
            self.ids.lbl_total_geral.text = "Preencha corretamente"
            return
        qtd = int(qtd_text)
        if qtd <= 0:
            self.ids.lbl_total_geral.text = "Quantidade inválida"
            return
        try:
            data_hora = datetime.now().strftime(FORMATO_DATA)
            conn = get_conn(); cur = conn.cursor()
            cur.execute("INSERT INTO impressoes (operador, usuario, impressora, quantidade, data_hora) VALUES (?, ?, ?, ?, ?)",
                        (operador, usuario, impressora, qtd, data_hora))
            conn.commit(); conn.close()
            logging.info("Impressão registrada: %s %s %s %d", operador, usuario, impressora, qtd)
            self.ids.input_qtd.text = ""
            self.usuario_selecionado(usuario)  # atualiza totais
        except Exception:
            logging.exception("Erro registrar impressao")
            self.ids.lbl_total_geral.text = "Erro ao gravar"

class RelatorioScreen(Screen):
    def gerar_relatorio(self):
        try:
            agora = datetime.now()
            mes_ini = agora.replace(day=1).date().isoformat()
            ano_ini = agora.replace(month=1, day=1).date().isoformat()
            hoje = agora.date().isoformat()
            conn = get_conn(); cur = conn.cursor()
            # total por impressora
            cur.execute("SELECT impressora, SUM(quantidade) FROM impressoes GROUP BY impressora")
            total = cur.fetchall()
            # mensal
            cur.execute("SELECT impressora, SUM(quantidade) FROM impressoes WHERE date(substr(data_hora,1,10)) BETWEEN date(?) AND date(?) GROUP BY impressora", (mes_ini, hoje))
            mensal = cur.fetchall()
            # anual
            cur.execute("SELECT impressora, SUM(quantidade) FROM impressoes WHERE date(substr(data_hora,1,10)) BETWEEN date(?) AND date(?) GROUP BY impressora", (ano_ini, hoje))
            anual = cur.fetchall()
            conn.close()
        except Exception:
            logging.exception("Erro gerar relatorio")
            total = mensal = anual = []

        texto = "[b]TOTAL POR IMPRESSORA[/b]\n"
        if total:
            for i, s in total:
                texto += f"{i}: {s or 0} páginas\n"
        else:
            texto += "Nenhum registro\n"
        texto += "\n[b]MENSAL (este mês)[/b]\n"
        if mensal:
            for i, s in mensal:
                texto += f"{i}: {s or 0} páginas\n"
        else:
            texto += "Nenhum registro\n"
        texto += "\n[b]ANUAL (este ano)[/b]\n"
        if anual:
            for i, s in anual:
                texto += f"{i}: {s or 0} páginas\n"
        else:
            texto += "Nenhum registro\n"
        self.ids.txt_relatorio.text = texto

# ---------- App ----------
class ControleImpressoesApp(App):
    usuario_logado = None
    nome_usuario = None

    def build(self):
        # cria DB e admin (se necessário)
        criar_tabelas_e_admin_padrao()
        # carregar KV root antes de manipular screens
        root = Builder.load_string(KV)
        # preencher spinner de operadores no login (safe, root já existe)
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT username FROM operadores ORDER BY username")
            ops = [r[0] for r in cur.fetchall()]
            conn.close()
        except Exception:
            logging.exception("Erro carregar operadores no build")
            ops = []
        login_screen = root.get_screen("login")
        if ops:
            login_screen.ids.spinner_operadores.values = ops
            login_screen.ids.spinner_operadores.text = ops[0]
        else:
            login_screen.ids.spinner_operadores.values = []
            login_screen.ids.spinner_operadores.text = "Nenhum operador"
        # save root
        self.root = root
        logging.info("Aplicação pronta. DB em: %s", DB_FILE)
        return root

    def preencher_registro(self):
        # helper para carregar spinners da tela de registro
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT nome FROM usuarios ORDER BY nome")
            usuarios = [r[0] for r in cur.fetchall()]
            cur.execute("SELECT nome FROM impressoras ORDER BY nome")
            impressoras = [r[0] for r in cur.fetchall()]
            conn.close()
        except Exception:
            logging.exception("Erro preencher registro")
            usuarios = []; impressoras = []
        reg = self.root.get_screen("registrar")
        if usuarios:
            reg.ids.spinner_usuario.values = usuarios
            reg.ids.spinner_usuario.text = usuarios[0]
        else:
            reg.ids.spinner_usuario.values = []
            reg.ids.spinner_usuario.text = "Selecione o usuário"
        if impressoras:
            reg.ids.spinner_impressora.values = impressoras
            reg.ids.spinner_impressora.text = impressoras[0]
        else:
            reg.ids.spinner_impressora.values = []
            reg.ids.spinner_impressora.text = "Selecione a impressora"
        # set operator label
        home = self.root.get_screen("home")
        home.ids.lbl_operador.text = f"Operador: {self.nome_usuario if self.nome_usuario else self.usuario_logado}"

# ---------- Run ----------
if __name__ == "__main__":
    logging.info("Start app")
    ControleImpressoesApp().run()
