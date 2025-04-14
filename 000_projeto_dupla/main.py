from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class MeuLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.texto_input = TextInput(hint_text="Digite algo aqui")
        self.add_widget(self.texto_input)

        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.mostrar_mensagem)
        self.add_widget(btn_ok)

        btn_fechar = Button(text="Fechar")
        btn_fechar.bind(on_press=self.fechar_app)
        self.add_widget(btn_fechar)

    def mostrar_mensagem(self, instance):
        texto = self.texto_input.text
        popup = Popup(title='Mensagem',
                      content=Label(text=f'Você digitou: {texto}'),
                      size_hint=(None, None), size=(300, 200))
        popup.open()

    def fechar_app(self, instance):
        App.get_running_app().stop()


class MeuApp(App):
    def build(self):
        return MeuLayout()


if __name__ == '__main__':
    MeuApp().run()
