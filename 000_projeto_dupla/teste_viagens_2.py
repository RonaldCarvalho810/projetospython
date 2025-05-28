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
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.core.window import Window

Window.size = (400, 650)
DB_NAME = "viagens.db"
FORMATO_DATA = "%d/%m/%Y %H:%M"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS viagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT NOT NULL,
            destino TEXT NOT NULL,
            data_hora_inicio TEXT NOT NULL,
            data_hora_fim TEXT,
            km_inicial INTEGER,
            km_final INTEGER,
            km_deslocado INTEGER,
            tempo_viagem TEXT
        )
    ''')
    conn.commit()
    conn.close()

class ViagemApp(App):
    def build(self):
        criar_tabela()
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.origem_input = TextInput(hint_text="Origem", multiline=False)
        self.destino_input = TextInput(hint_text="Destino", multiline=False)
        self.km_inicial_input = TextInput(hint_text="KM Inicial", multiline=False, input_filter='int')
        self.data_hora_inicio_input = TextInput(hint_text="Data e Hora de Início (DD/MM/AAAA HH:MM)", multiline=False)

        self.layout_principal.add_widget(self.origem_input)
        self.layout_principal.add_widget(self.destino_input)
        self.layout_principal.add_widget(self.km_inicial_input)
        self.layout_principal.add_widget(self.data_hora_inicio_input)

        self.btn_adicionar = Button(text="Adicionar Viagem")
        self.btn_adicionar.bind(on_press=self.adicionar_viagem)
        self.layout_principal.add_widget(self.btn_adicionar)

        self.btn_relatorio = Button(text="Gerar Relatório")
        self.btn_relatorio.bind(on_press=self.gerar_relatorio)
        self.layout_principal.add_widget(self.btn_relatorio)

        self.scrollview = ScrollView()
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scrollview.add_widget(self.grid)
        self.layout_principal.add_widget(self.scrollview)

        self.carregar_viagens()
        return self.layout_principal

    def adicionar_viagem(self, instance):
        origem = self.origem_input.text.strip()
        destino = self.destino_input.text.strip()
        km_inicial = self.km_inicial_input.text.strip()
        data_inicio = self.data_hora_inicio_input.text.strip()

        if not origem or not destino or not data_inicio or not km_inicial:
            self.mostrar_popup("Erro", "Preencha todos os campos.")
            return

        try:
            data_formatada = datetime.strptime(data_inicio, FORMATO_DATA).strftime(FORMATO_DATA)
        except ValueError:
            self.mostrar_popup("Erro", "Formato de data inválido. Use DD/MM/AAAA HH:MM.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO viagens (origem, destino, data_hora_inicio, km_inicial) VALUES (?, ?, ?, ?)', 
                       (origem, destino, data_formatada, int(km_inicial)))
        conn.commit()
        conn.close()

        self.origem_input.text = ""
        self.destino_input.text = ""
        self.km_inicial_input.text = ""
        self.data_hora_inicio_input.text = ""

        self.carregar_viagens()

    def carregar_viagens(self):
        self.grid.clear_widgets()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, origem, destino, data_hora_inicio, data_hora_fim, km_inicial, km_final, km_deslocado, tempo_viagem FROM viagens ORDER BY id DESC')
        viagens = cursor.fetchall()
        conn.close()

        for viagem in viagens:
            texto = f"ID: {viagem[0]}\nOrigem: {viagem[1]}\nDestino: {viagem[2]}\nInício: {viagem[3]}\nKM Inicial: {viagem[5]}"
            if viagem[4]:
                texto += f"\nFim: {viagem[4]}\nKM Final: {viagem[6]}\nDeslocado: {viagem[7]} km\nDuração: {viagem[8]}"
            else:
                texto += "\n[Fim não informado]"

            btn = Button(text=texto, size_hint_y=None, height=180)
            btn.bind(on_press=lambda inst, vid=viagem[0]: self.adicionar_fim_viagem(vid))
            self.grid.add_widget(btn)

    def adicionar_fim_viagem(self, id_viagem):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_fim = TextInput(hint_text="Data e Hora de Fim (DD/MM/AAAA HH:MM)", multiline=False)
        input_km_final = TextInput(hint_text="KM Final", multiline=False, input_filter='int')
        btn_salvar = Button(text="Salvar")

        content.add_widget(Label(text=f"Finalizar viagem ID {id_viagem}:"))
        content.add_widget(input_fim)
        content.add_widget(input_km_final)
        content.add_widget(btn_salvar)

        popup = Popup(title="Finalizar Viagem", content=content, size_hint=(0.9, 0.6))

        def salvar(instance):
            fim = input_fim.text.strip()
            km_final = input_km_final.text.strip()
            if fim and km_final:
                try:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute('SELECT data_hora_inicio, km_inicial FROM viagens WHERE id = ?', (id_viagem,))
                    resultado = cursor.fetchone()
                    if resultado:
                        data_inicio_str, km_inicial = resultado
                        inicio_dt = datetime.strptime(data_inicio_str, FORMATO_DATA)
                        fim_dt = datetime.strptime(fim, FORMATO_DATA)
                        duracao = fim_dt - inicio_dt
                        km_deslocado = int(km_final) - km_inicial
                        tempo_viagem = str(duracao)
                        fim_formatado = fim_dt.strftime(FORMATO_DATA)

                        cursor.execute('''
                            UPDATE viagens 
                            SET data_hora_fim = ?, km_final = ?, km_deslocado = ?, tempo_viagem = ?
                            WHERE id = ?
                        ''', (fim_formatado, int(km_final), km_deslocado, tempo_viagem, id_viagem))

                        conn.commit()
                        conn.close()
                        popup.dismiss()
                        self.carregar_viagens()
                    else:
                        self.mostrar_popup("Erro", "Viagem não encontrada.")
                except ValueError:
                    self.mostrar_popup("Erro", "Formato de data inválido. Use DD/MM/AAAA HH:MM.")
                except Exception as e:
                    self.mostrar_popup("Erro", f"Ocorreu um erro: {e}")
            else:
                self.mostrar_popup("Erro", "Preencha todos os campos.")

        btn_salvar.bind(on_press=salvar)
        popup.open()

    def gerar_relatorio(self, instance):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, origem, destino, data_hora_inicio, data_hora_fim, km_inicial, km_final, km_deslocado, tempo_viagem FROM viagens')
        viagens = cursor.fetchall()
        conn.close()

        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Viagens</title>
            <style>
                body { font-family: Arial; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h2>Relatório de Viagens</h2>
            <h3>Câmara de Dores do Turvo</h3>
            <table>
                <tr>
                    <th>ID</th><th>Origem</th><th>Destino</th><th>Início</th><th>Fim</th>
                    <th>KM Inicial</th><th>KM Final</th><th>KM Deslocado</th><th>Tempo</th>
                </tr>
        """

        for v in viagens:
            html += f"""
                <tr>
                    <td>{v[0]}</td>
                    <td>{v[1]}</td>
                    <td>{v[2]}</td>
                    <td>{v[3]}</td>
                    <td>{v[4] if v[4] else '-'}</td>
                    <td>{v[5] if v[5] else '-'}</td>
                    <td>{v[6] if v[6] else '-'}</td>
                    <td>{v[7] if v[7] else '-'}</td>
                    <td>{v[8] if v[8] else '-'}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        caminho_arquivo = "relatorio_viagens.html"
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
    ViagemApp().run()
