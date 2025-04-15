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

    # Cria a tabela com as novas colunas km_inicial e km_final
    cursor.execute('''CREATE TABLE IF NOT EXISTS viagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origem TEXT NOT NULL,
        destino TEXT NOT NULL,
        data_hora_inicio TEXT NOT NULL,
        data_hora_fim TEXT,
        km_inicial REAL NOT NULL DEFAULT 0,
        km_final REAL
    )''')

    conn.commit()
    conn.close()

class ViagemApp(App):
    def build(self):
        criar_tabela()
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.origem_input = TextInput(hint_text="Origem", multiline=False)
        self.destino_input = TextInput(hint_text="Destino", multiline=False)
        self.data_hora_inicio_input = TextInput(hint_text="Data e Hora de Início (YYYY-MM-DD HH:MM)", multiline=False)
        self.km_inicial_input = TextInput(hint_text="Km Inicial", multiline=False, input_filter='int')

        self.layout_principal.add_widget(self.origem_input)
        self.layout_principal.add_widget(self.destino_input)
        self.layout_principal.add_widget(self.data_hora_inicio_input)
        self.layout_principal.add_widget(self.km_inicial_input)

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
        km_inicial = self.km_inicial_input.text.strip()

        if not origem or not destino or not data_inicio or not km_inicial:
            self.mostrar_popup("Erro", "Preencha todos os campos obrigatórios.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO viagens (origem, destino, data_hora_inicio, km_inicial) VALUES (?, ?, ?, ?)', 
                       (origem, destino, data_inicio, km_inicial))
        conn.commit()
        conn.close()

        self.origem_input.text = ""
        self.destino_input.text = ""
        self.data_hora_inicio_input.text = ""
        self.km_inicial_input.text = ""

        self.carregar_viagens()

    def carregar_viagens(self):
        self.grid.clear_widgets()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, origem, destino, data_hora_inicio, data_hora_fim, km_inicial, km_final FROM viagens ORDER BY id DESC')
        viagens = cursor.fetchall()
        conn.close()

        for viagem in viagens:
            texto = f"ID: {viagem[0]}\nOrigem: {viagem[1]}\nDestino: {viagem[2]}\nInício: {viagem[3]}\nKm Inicial: {viagem[5]}"
            if viagem[6]:
                texto += f"\nKm Final: {viagem[6]}"
            else:
                texto += "\nKm Final: [não informado]"

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
        input_km_final = TextInput(hint_text="Km Final", multiline=False, input_filter='int')
        btn_salvar = Button(text="Salvar")

        content.add_widget(Label(text=f"Finalizar viagem ID {id_viagem}:"))
        content.add_widget(input_fim)
        content.add_widget(input_km_final)
        content.add_widget(btn_salvar)

        popup = Popup(title="Finalizar Viagem", content=content, size_hint=(0.9, 0.5))

        def salvar(instance):
            fim = input_fim.text.strip()
            km_final = input_km_final.text.strip()

            if fim and km_final:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('UPDATE viagens SET data_hora_fim = ?, km_final = ? WHERE id = ?', (fim, km_final, id_viagem))
                conn.commit()
                conn.close()
                popup.dismiss()
                self.carregar_viagens()
            else:
                self.mostrar_popup("Erro", "Preencha a data e hora de fim, e a quilometragem final.")

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
