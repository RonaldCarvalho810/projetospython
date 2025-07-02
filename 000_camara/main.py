import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

DB_PATH = "ouvidoria.db"

def criar_tabela():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manifestacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            datahora TEXT NOT NULL,
            status TEXT NOT NULL,
            meio TEXT NOT NULL,
            prazo TEXT NOT NULL,
            resposta TEXT,
            servidor TEXT,
            dataresposta TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

class OuvidoriaLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10)

        self.add_widget(Label(text='Nome do cidadão:'))
        self.nome_input = TextInput()
        self.add_widget(self.nome_input)

        self.add_widget(Label(text='Tipo de manifestação:'))
        self.tipo_spinner = Spinner(
            text='Selecione',
            values=['Denúncia', 'Reclamação', 'Sugestão', 'Elogio', 'Solicitação']
        )
        self.add_widget(self.tipo_spinner)

        self.add_widget(Label(text='Descrição:'))
        self.descricao_input = TextInput()
        self.add_widget(self.descricao_input)

        self.add_widget(Label(text='Meio de entrada:'))
        self.meio_spinner = Spinner(
            text='Selecione',
            values=['Presencial', 'Telefone', 'Site', 'WhatsApp', 'E-mail']
        )
        self.add_widget(self.meio_spinner)

        self.add_widget(Label(text='Dias para resposta:'))
        self.dias_input = TextInput()
        self.dias_input.bind(text=self.calcular_prazo)
        self.add_widget(self.dias_input)

        self.add_widget(Label(text='Prazo final (calculado):'))
        self.prazo_input = TextInput(readonly=True)
        self.add_widget(self.prazo_input)

        self.add_widget(Label(text='Status:'))
        self.status_spinner = Spinner(
            text='Pendente',
            values=['Pendente', 'Em andamento', 'Finalizado']
        )
        self.add_widget(self.status_spinner)

        self.add_widget(Label(text='Servidor responsável:'))
        self.servidor_input = TextInput()
        self.add_widget(self.servidor_input)

        self.add_widget(Label(text='Resposta da ouvidoria:'))
        self.resposta_input = TextInput()
        self.add_widget(self.resposta_input)

        self.btn_salvar = Button(text='Salvar Manifestação')
        self.btn_salvar.bind(on_press=self.salvar_manifestacao)
        self.add_widget(self.btn_salvar)

        self.btn_listar = Button(text='Listar / Alterar')
        self.btn_listar.bind(on_press=self.listar_manifestacoes)
        self.add_widget(self.btn_listar)

        self.btn_pdf = Button(text='Gerar PDF')
        self.btn_pdf.bind(on_press=self.gerar_pdf)
        self.add_widget(self.btn_pdf)

        self.resultado = Label(text='')
        self.add_widget(self.resultado)

    def calcular_prazo(self, instance, value):
        try:
            dias = int(value)
            data_final = datetime.now() + timedelta(days=dias)
            self.prazo_input.text = data_final.strftime('%d/%m/%Y')
        except:
            self.prazo_input.text = ''

    def salvar_manifestacao(self, instance):
        nome = self.nome_input.text.strip()
        tipo = self.tipo_spinner.text
        descricao = self.descricao_input.text.strip()
        meio = self.meio_spinner.text
        prazo = self.prazo_input.text
        status = self.status_spinner.text
        servidor = self.servidor_input.text.strip()
        resposta = self.resposta_input.text.strip()
        datahora = datetime.now().strftime('%d/%m/%Y %H:%M')

        if not nome or tipo == 'Selecione' or not descricao or meio == 'Selecione' or not prazo:
            self.resultado.text = "Preencha todos os campos obrigatórios!"
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO manifestacoes (nome, tipo, descricao, datahora, status, meio, prazo, resposta, servidor, dataresposta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, tipo, descricao, datahora, status, meio, prazo, resposta, servidor, None))
        conexao.commit()
        conexao.close()

        self.resultado.text = "Manifestação salva com sucesso!"
        self.nome_input.text = ''
        self.tipo_spinner.text = 'Selecione'
        self.descricao_input.text = ''
        self.meio_spinner.text = 'Selecione'
        self.dias_input.text = ''
        self.prazo_input.text = ''
        self.status_spinner.text = 'Pendente'
        self.servidor_input.text = ''
        self.resposta_input.text = ''

    def listar_manifestacoes(self, instance):
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, tipo, descricao, datahora, status, meio, prazo, resposta, servidor, dataresposta FROM manifestacoes ORDER BY id DESC')
        registros = cursor.fetchall()
        conexao.close()

        box = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        for reg in registros:
            texto = (
                f"[b]ID:[/b] {reg[0]}  [b]Nome:[/b] {reg[1]}  [b]Tipo:[/b] {reg[2]}\n"
                f"[b]Data:[/b] {reg[4]}  [b]Status:[/b] {reg[5]}  [b]Meio:[/b] {reg[6]}\n"
                f"[b]Prazo:[/b] {reg[7]}  [b]Servidor:[/b] {reg[9]}\n"
                f"[b]Resposta:[/b] {reg[8] or '---'}\n"
                f"[b]Data Resposta:[/b] {reg[10] or '---'}\n"
                f"[b]Descrição:[/b] {reg[3]}"
            )
            label = Label(text=texto, markup=True, size_hint_y=None, height=240)
            box.add_widget(label)

            btn_alterar = Button(text=f"Responder / Alterar ID {reg[0]}", size_hint_y=None, height=40)
            btn_alterar.bind(on_press=lambda inst, r=reg: self.popup_editar(r))
            box.add_widget(btn_alterar)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(box)

        popup = Popup(title="Manifestações", content=scroll, size_hint=(0.95, 0.95))
        popup.open()

    def popup_editar(self, reg):
        layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        status_spinner = Spinner(text=reg[5], values=['Pendente', 'Em andamento', 'Finalizado'])
        resposta_input = TextInput(text=reg[8] or '', hint_text="Resposta da Ouvidoria")

        salvar = Button(text="Salvar Alterações")
        layout.add_widget(Label(text=f"ID {reg[0]} - {reg[1]}"))
        layout.add_widget(Label(text="Status:"))
        layout.add_widget(status_spinner)
        layout.add_widget(Label(text="Resposta:"))
        layout.add_widget(resposta_input)
        layout.add_widget(salvar)

        popup = Popup(title="Responder Manifestação", content=layout, size_hint=(0.9, 0.7))

        def salvar_alteracoes(instance):
            novo_status = status_spinner.text
            nova_resposta = resposta_input.text.strip()
            dataresposta = datetime.now().strftime('%d/%m/%Y %H:%M')

            conexao = sqlite3.connect(DB_PATH)
            cursor = conexao.cursor()
            cursor.execute('''
                UPDATE manifestacoes
                SET status = ?, resposta = ?, dataresposta = ?
                WHERE id = ?
            ''', (novo_status, nova_resposta, dataresposta, reg[0]))
            conexao.commit()
            conexao.close()
            popup.dismiss()

        salvar.bind(on_press=salvar_alteracoes)
        popup.open()

    def gerar_pdf(self, instance):
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute('SELECT nome, tipo, descricao, datahora, status, meio, prazo, resposta, servidor, dataresposta FROM manifestacoes ORDER BY id DESC')
        registros = cursor.fetchall()
        conexao.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório - Ouvidoria", ln=True, align='C')
        pdf.ln(10)

        for reg in registros:
            pdf.multi_cell(0, 10,
                f"Nome: {reg[0]}\nTipo: {reg[1]}\nDescrição: {reg[2]}\nData: {reg[3]}\nStatus: {reg[4]}"
                f"\nMeio: {reg[5]}\nPrazo: {reg[6]}\nResposta: {reg[7] or '---'}\nServidor: {reg[8]}\nData Resposta: {reg[9] or '---'}\n")
            pdf.ln(5)

        path = os.path.join(os.getcwd(), 'relatorio_ouvidoria.pdf')
        pdf.output(path)
        self.resultado.text = "PDF gerado com sucesso."

class OuvidoriaApp(App):
    def build(self):
        criar_tabela()
        return OuvidoriaLayout()

if __name__ == '__main__':
    OuvidoriaApp().run()
