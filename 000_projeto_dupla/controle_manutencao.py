import sqlite3
import webbrowser
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.core.window import Window

Window.size = (400, 650)
DB_NAME = "manutencoes.db"
FORMATO_DATA = "%d/%m/%Y"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            data TEXT NOT NULL,
            km INTEGER,
            oficina TEXT,
            servicos TEXT,
            observacoes TEXT
        )
    ''')
    conn.commit()
    conn.close()

class ManutencaoApp(App):
    def build(self):
        criar_tabela()
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.placa_input = TextInput(hint_text="Placa do Carro", multiline=False)
        self.data_input = TextInput(hint_text="Data (DD/MM/AAAA)", multiline=False)
        self.km_input = TextInput(hint_text="KM", multiline=False, input_filter='int')
        self.oficina_input = TextInput(hint_text="Oficina", multiline=False)
        self.servicos_input = TextInput(hint_text="Serviços Feitos", multiline=True)
        self.obs_input = TextInput(hint_text="Observações", multiline=True)

        self.layout_principal.add_widget(self.placa_input)
        self.layout_principal.add_widget(self.data_input)
        self.layout_principal.add_widget(self.km_input)
        self.layout_principal.add_widget(self.oficina_input)
        self.layout_principal.add_widget(self.servicos_input)
        self.layout_principal.add_widget(self.obs_input)

        self.btn_adicionar = Button(text="Adicionar Manutenção")
        self.btn_adicionar.bind(on_press=self.adicionar_manutencao)
        self.layout_principal.add_widget(self.btn_adicionar)

        self.btn_relatorio = Button(text="Gerar Relatório")
        self.btn_relatorio.bind(on_press=self.gerar_relatorio)
        self.layout_principal.add_widget(self.btn_relatorio)

        self.scrollview = ScrollView()
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scrollview.add_widget(self.grid)
        self.layout_principal.add_widget(self.scrollview)

        self.carregar_manutencoes()
        return self.layout_principal

    def adicionar_manutencao(self, instance):
        placa = self.placa_input.text.strip()
        data = self.data_input.text.strip()
        km = self.km_input.text.strip()
        oficina = self.oficina_input.text.strip()
        servicos = self.servicos_input.text.strip()
        obs = self.obs_input.text.strip()

        if not placa or not data or not km:
            self.mostrar_popup("Erro", "Preencha pelo menos placa, data e KM.")
            return

        try:
            data_formatada = datetime.strptime(data, FORMATO_DATA).strftime(FORMATO_DATA)
        except ValueError:
            self.mostrar_popup("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO manutencoes (placa, data, km, oficina, servicos, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (placa, data_formatada, int(km), oficina, servicos, obs))
        conn.commit()
        conn.close()

        self.placa_input.text = ""
        self.data_input.text = ""
        self.km_input.text = ""
        self.oficina_input.text = ""
        self.servicos_input.text = ""
        self.obs_input.text = ""

        self.carregar_manutencoes()

    def carregar_manutencoes(self):
        self.grid.clear_widgets()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, placa, data, km, oficina, servicos, observacoes FROM manutencoes ORDER BY id DESC')
        registros = cursor.fetchall()
        conn.close()

        for m in registros:
            texto = f"ID: {m[0]}\nPlaca: {m[1]}\nData: {m[2]}\nKM: {m[3]}\nOficina: {m[4]}\nServiços: {m[5]}\nObs: {m[6]}"
            btn = Button(text=texto, size_hint_y=None, height=200)
            self.grid.add_widget(btn)

    def gerar_relatorio(self, instance):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM manutencoes')
        manutencoes = cursor.fetchall()
        conn.close()

        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Abastecimentos e Manutenções</title>
            <style>
                body { font-family: Arial; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h2>Relatório de Abastecimentos e Manutenções</h2>
            <table>
                <tr>
                    <th>ID</th><th>Placa</th><th>Data</th><th>KM</th><th>Oficina</th>
                    <th>Serviços</th><th>Observações</th>
                </tr>
        """

        for m in manutencoes:
            html += f"""
                <tr>
                    <td>{m[0]}</td>
                    <td>{m[1]}</td>
                    <td>{m[2]}</td>
                    <td>{m[3]}</td>
                    <td>{m[4]}</td>
                    <td>{m[5]}</td>
                    <td>{m[6]}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        caminho_arquivo = "relatorio_manutencoes.html"
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(caminho_arquivo)

    def mostrar_popup(self, titulo, mensagem):
        view = ModalView(size_hint=(0.8, 0.3))
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="Fechar", size_hint=(1, 0.4))
        btn.bind(on_press=view.dismiss)
        box.add_widget(btn)
        view.add_widget(box)
        view.open()

if __name__ == "__main__":
    ManutencaoApp().run()
