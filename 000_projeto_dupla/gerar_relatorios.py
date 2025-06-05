import sqlite3
import pdfkit
import os
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

Window.size = (450, 700)

DB_VIAGENS = "viagens.db"
DB_MANUTENCOES = "manutencoes.db"
FORMATO_DATA = "%d/%m/%Y"

def criar_tabela_viagens():
    conn = sqlite3.connect(DB_VIAGENS)
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

def criar_tabela_manutencoes():
    conn = sqlite3.connect(DB_MANUTENCOES)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            data TEXT NOT NULL,
            km INTEGER NOT NULL,
            oficina TEXT NOT NULL,
            servicos TEXT NOT NULL,
            observacoes TEXT
        )
    ''')
    conn.commit()
    conn.close()

class RelatorioApp(App):
    def build(self):
        criar_tabela_viagens()
        criar_tabela_manutencoes()

        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Período para viagens
        periodo_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.data_inicio_input = TextInput(hint_text="Data Início (dd/mm/aaaa)", multiline=False)
        self.data_fim_input = TextInput(hint_text="Data Fim (dd/mm/aaaa)", multiline=False)
        periodo_box.add_widget(self.data_inicio_input)
        periodo_box.add_widget(self.data_fim_input)
        self.layout_principal.add_widget(periodo_box)

        self.btn_gerar_viagens = Button(text="Gerar Relatório de Viagens (por Período)", size_hint_y=None, height=50)
        self.btn_gerar_viagens.bind(on_press=self.gerar_relatorio_viagens)
        self.layout_principal.add_widget(self.btn_gerar_viagens)

        self.btn_gerar_manutencoes = Button(text="Gerar Relatório de Manutenções", size_hint_y=None, height=50)
        self.btn_gerar_manutencoes.bind(on_press=self.gerar_relatorio_manutencoes)
        self.layout_principal.add_widget(self.btn_gerar_manutencoes)

        self.label_status = Label(text="", size_hint_y=None, height=30)
        self.layout_principal.add_widget(self.label_status)

        return self.layout_principal

    def mostrar_popup(self, titulo, mensagem):
        view = ModalView(size_hint=(0.8, 0.3))
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="Fechar", size_hint=(1, 0.4))
        btn.bind(on_press=view.dismiss)
        box.add_widget(btn)
        view.add_widget(box)
        view.open()

    def gerar_relatorio_viagens(self, instance):
        data_inicio_str = self.data_inicio_input.text.strip()
        data_fim_str = self.data_fim_input.text.strip()

        try:
            data_inicio = datetime.strptime(data_inicio_str, FORMATO_DATA) if data_inicio_str else None
            data_fim = datetime.strptime(data_fim_str, FORMATO_DATA) if data_fim_str else None
        except ValueError:
            self.mostrar_popup("Erro", "Formato de data inválido. Use dd/mm/aaaa.")
            return

        conn = sqlite3.connect(DB_VIAGENS)
        cursor = conn.cursor()

        if data_inicio and data_fim:
            cursor.execute('''
                SELECT id, origem, destino, data_hora_inicio, data_hora_fim, km_inicial, km_final, km_deslocado, tempo_viagem 
                FROM viagens
            ''')
            viagens = cursor.fetchall()
            # Filtrar pela data no Python porque data_hora_inicio é string com hora
            viagens_filtradas = []
            for v in viagens:
                dt_inicio = datetime.strptime(v[3], "%d/%m/%Y %H:%M")
                if data_inicio <= dt_inicio.date() <= data_fim:
                    viagens_filtradas.append(v)
            if not viagens_filtradas:
                viagens_filtradas = viagens
        else:
            cursor.execute('SELECT id, origem, destino, data_hora_inicio, data_hora_fim, km_inicial, km_final, km_deslocado, tempo_viagem FROM viagens')
            viagens_filtradas = cursor.fetchall()

        conn.close()

        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Viagens</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h2, h3 { text-align: center; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #aaa; padding: 8px; text-align: center; }
                th { background-color: #ddd; }
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

        for v in viagens_filtradas:
            fim = v[4] if v[4] else "/"
            km_final = v[6] if v[6] is not None else "/"
            km_deslocado = v[7] if v[7] is not None else "/"
            tempo = v[8] if v[8] else "/"
            html += f"""
                <tr>
                    <td>{v[0]}</td>
                    <td>{v[1]}</td>
                    <td>{v[2]}</td>
                    <td>{v[3]}</td>
                    <td>{fim}</td>
                    <td>{v[5]}</td>
                    <td>{km_final}</td>
                    <td>{km_deslocado}</td>
                    <td>{tempo}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        caminho_html = "relatorio_viagens.html"
        caminho_pdf = "relatorio_viagens.pdf"
        with open(caminho_html, "w", encoding="utf-8") as f:
            f.write(html)

        try:
            pdfkit.from_file(caminho_html, caminho_pdf)
            self.label_status.text = "Relatório PDF de viagens gerado com sucesso!"
            webbrowser.open(caminho_pdf)
        except Exception as e:
            self.mostrar_popup("Erro", f"Falha ao gerar PDF: {e}")

    def gerar_relatorio_manutencoes(self, instance):
        conn = sqlite3.connect(DB_MANUTENCOES)
        cursor = conn.cursor()
        cursor.execute('SELECT id, placa, data, km, oficina, servicos, observacoes FROM manutencoes')
        manutencoes = cursor.fetchall()
        conn.close()

        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Manutenções</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h2, h3 { text-align: center; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #aaa; padding: 8px; text-align: center; }
                th { background-color: #ddd; }
            </style>
        </head>
        <body>
            <h2>Relatório de Manutenções</h2>
            <h3>Câmara de Dores do Turvo</h3>
            <table>
                <tr>
                    <th>ID</th><th>Placa</th><th>Data</th><th>KM</th><th>Oficina</th><th>Serviços</th><th>Observações</th>
                </tr>
        """

        for m in manutencoes:
            obs = m[6] if m[6] else "/"
            html += f"""
                <tr>
                    <td>{m[0]}</td>
                    <td>{m[1]}</td>
                    <td>{m[2]}</td>
                    <td>{m[3]}</td>
                    <td>{m[4]}</td>
                    <td>{m[5]}</td>
                    <td>{obs}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        caminho_html = "relatorio_manutencoes.html"
        caminho_pdf = "relatorio_manutencoes.pdf"
        with open(caminho_html, "w", encoding="utf-8") as f:
            f.write(html)

        try:
            pdfkit.from_file(caminho_html, caminho_pdf)
            self.label_status.text = "Relatório PDF de manutenções gerado com sucesso!"
            webbrowser.open(caminho_pdf)
        except Exception as e:
            self.mostrar_popup("Erro", f"Falha ao gerar PDF: {e}")

if __name__ == "__main__":
    RelatorioApp().run()
