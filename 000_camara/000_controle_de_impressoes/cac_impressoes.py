import sqlite3
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty

# -----------------------------------------------------------
# BANCO DE DADOS
# -----------------------------------------------------------
def init_db():
    conn = sqlite3.connect("impressoes.db")
    c = conn.cursor()

    # Usuários (login)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Impressões registradas
    c.execute("""
        CREATE TABLE IF NOT EXISTS prints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            printer TEXT NOT NULL,
            qtd INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Usuário padrão
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (name, password) VALUES ('admin', '123')")
        c.execute("INSERT INTO users (name, password) VALUES ('ronald', '1')")

    conn.commit()
    conn.close()

# -----------------------------------------------------------
# TELAS
# -----------------------------------------------------------
class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    username = StringProperty("")

class RegistrarScreen(Screen):
    spinner_user = ObjectProperty(None)
    spinner_printer = ObjectProperty(None)
    qtd_input = ObjectProperty(None)

    def registrar(self):
        user = self.spinner_user.text
        printer = self.spinner_printer.text
        qtd = self.qtd_input.text.strip()

        if not user or not printer or not qtd.isdigit():
            return

        conn = sqlite3.connect("impressoes.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO prints (user, printer, qtd, date) VALUES (?, ?, ?, ?)",
            (user, printer, int(qtd), datetime.now().strftime("%Y-%m-%d"))
        )
        conn.commit()
        conn.close()

        self.qtd_input.text = ""

class ConsultaScreen(Screen):
    texto_resultado = ObjectProperty(None)

    def consultar(self):
        conn = sqlite3.connect("impressoes.db")
        c = conn.cursor()

        # MENSAL (mês atual)
        mes_atual = datetime.now().strftime("%Y-%m")
        c.execute("""
            SELECT printer, SUM(qtd)
            FROM prints
            WHERE date LIKE ?
            GROUP BY printer
        """, (mes_atual + "%",))
        mensal = c.fetchall()

        # ANUAL (ano atual)
        ano_atual = datetime.now().strftime("%Y")
        c.execute("""
            SELECT printer, SUM(qtd)
            FROM prints
            WHERE date LIKE ?
            GROUP BY printer
        """, (ano_atual + "%",))
        anual = c.fetchall()

        conn.close()

        texto = "[b]ACUMULADO MENSAL[/b]\n"
        if mensal:
            for p, t in mensal:
                texto += f"{p}: {t} páginas\n"
        else:
            texto += "Nenhum registro.\n"

        texto += "\n[b]ACUMULADO ANUAL[/b]\n"
        if anual:
            for p, t in anual:
                texto += f"{p}: {t} páginas\n"
        else:
            texto += "Nenhum registro.\n"

        self.texto_resultado.text = texto


# -----------------------------------------------------------
# KV CODE
# -----------------------------------------------------------
kv = """
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    transition: NoTransition()
    LoginScreen:
    HomeScreen:
    RegistrarScreen:
    ConsultaScreen:

<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: 24
        spacing: 12

        Label:
            text: "Controle de Impressões - Login"
            font_size: 22
            size_hint_y: None
            height: 40

        Spinner:
            id: combo_users
            text: "Selecione o usuário"
            values: []
            size_hint_y: None
            height: 44

        TextInput:
            id: password
            hint_text: "Senha"
            password: True
            multiline: False
            size_hint_y: None
            height: 40     # <<< AQUI DIMINUI O TAMANHO DO CAMPO

        Button:
            text: "Entrar"
            size_hint_y: None
            height: 44
            on_release:
                app.verificar_login(combo_users.text, password.text)

<HomeScreen>:
    name: "home"
    username: ""
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        Label:
            text: "Bem vindo: " + root.username
            font_size: 20

        Button:
            text: "Registrar Impressões"
            on_release: app.root.current = "registrar"

        Button:
            text: "Consultar Acumulado (Mensal / Anual)"
            on_release: app.root.current = "consulta"

        Button:
            text: "Sair"
            on_release: app.root.current = "login"

<RegistrarScreen>:
    name: "registrar"
    spinner_user: spinner_user
    spinner_printer: spinner_printer
    qtd_input: qtd_input

    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        Label:
            text: "Registrar Impressões"
            font_size: 20

        Spinner:
            id: spinner_user
            text: "Usuário"
            values: []
            size_hint_y: None
            height: 40

        Spinner:
            id: spinner_printer
            text: "Impressora"
            values: ["HP", "Epson", "Canon", "Brother"]
            size_hint_y: None
            height: 40

        TextInput:
            id: qtd_input
            hint_text: "Quantidade"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: 40

        Button:
            text: "Registrar"
            size_hint_y: None
            height: 44
            on_release: root.registrar()

        Button:
            text: "Voltar"
            on_release: app.root.current = "home"

<ConsultaScreen>:
    name: "consulta"
    texto_resultado: texto_resultado

    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        Label:
            text: "Consultas de Impressões"
            font_size: 20

        Button:
            text: "Atualizar"
            size_hint_y: None
            height: 40
            on_release: root.consultar()

        ScrollView:
            size_hint_y: 1

            Label:
                id: texto_resultado
                text: ""
                markup: True
                size_hint_y: None
                height: self.texture_size[1]

        Button:
            text: "Voltar"
            on_release: app.root.current = "home"
"""

# -----------------------------------------------------------
# APP
# -----------------------------------------------------------
class MainApp(App):

    def build(self):
        init_db()
        root = Builder.load_string(kv)

        # Preenche usuários no login
        conn = sqlite3.connect("impressoes.db")
        c = conn.cursor()
        c.execute("SELECT name FROM users")
        nomes = [n[0] for n in c.fetchall()]
        conn.close()

        login_screen = root.get_screen("login")
        login_screen.ids.combo_users.values = nomes

        return root

    def verificar_login(self, usuario, senha):
        conn = sqlite3.connect("impressoes.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name=? AND password=?", (usuario, senha))
        ok = c.fetchone()
        conn.close()

        if ok:
            home = self.root.get_screen("home")
            home.username = usuario
            self.root.current = "home"

        else:
            print("Login incorreto!")

# -----------------------------------------------------------
MainApp().run()
