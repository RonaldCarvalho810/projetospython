import sqlite3
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

Window.size = (400, 600)

DB_NAME = "viagens.db"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS viagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT NOT NULL,
            destino TEXT NOT NULL,
            data_hora_inicio TEXT NOT NULL,
            data_hora_fim TEXT
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
        self.data_hora_inicio_input = TextInput(hint_text="Data e Hora de Início (YYYY-MM-DD HH:MM)", multiline=False)

        self.layout_principal.add_widget(self.origem_input)
        self.layout_principal.add_widget(self.destino_input)
        self.layout_principal.add_widget(self.data_hora_inicio_input)

        self.btn_adicionar = Button(text="Adicionar Viagem")
        self.btn_adicionar.bind(on_press=self.adicionar_viagem)
        self.layout_principal.add_widget(self.btn_adicionar)

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
        data_inicio = self.data_hora_inicio_input.text.strip()

        if not origem or not destino or not data_inicio:
            self.mostrar_popup("Erro", "Preencha todos os campos.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO viagens (origem, destino, data_hora_inicio) VALUES (?, ?, ?)', 
                       (origem, destino, data_inicio))
        conn.commit()
        conn.close()

        self.origem_input.text = ""
        self.destino_input.text = ""
        self.data_hora_inicio_input.text = ""

        self.carregar_viagens()

    def carregar_viagens(self):
        self.grid.clear_widgets()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, origem, destino, data_hora_inicio, data_hora_fim FROM viagens ORDER BY id DESC')
        viagens = cursor.fetchall()
        conn.close()

        for viagem in viagens:
            texto = f"ID: {viagem[0]}\nOrigem: {viagem[1]}\nDestino: {viagem[2]}\nInício: {viagem[3]}"
            if viagem[4]:
                texto += f"\nFim: {viagem[4]}"
            else:
                texto += "\n[Fim não informado]"

            btn = Button(text=texto, size_hint_y=None, height=140)
            btn.bind(on_press=lambda inst, vid=viagem[0]: self.adicionar_fim_viagem(vid))
            self.grid.add_widget(btn)

    def adicionar_fim_viagem(self, id_viagem):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_fim = TextInput(hint_text="Data e Hora de Fim (YYYY-MM-DD HH:MM)", multiline=False)
        btn_salvar = Button(text="Salvar")

        content.add_widget(Label(text=f"Finalizar viagem ID {id_viagem}:"))
        content.add_widget(input_fim)
        content.add_widget(btn_salvar)

        popup = Popup(title="Finalizar Viagem", content=content, size_hint=(0.9, 0.5))

        def salvar(instance):
            fim = input_fim.text.strip()
            if fim:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('UPDATE viagens SET data_hora_fim = ? WHERE id = ?', (fim, id_viagem))
                conn.commit()
                conn.close()
                popup.dismiss()
                self.carregar_viagens()
            else:
                self.mostrar_popup("Erro", "Preencha a data e hora de fim.")

        btn_salvar.bind(on_press=salvar)
        popup.open()

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
