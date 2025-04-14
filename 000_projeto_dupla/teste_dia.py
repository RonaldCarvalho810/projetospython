from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker

class MainApp(MDApp):
    def build(self):
        return

    def on_start(self):
        # Abre o calendário ao iniciar e chama o método para manipular a data escolhida
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.data_selecionada)
        date_picker.open()

    def data_selecionada(self, instance, value, date_range):
        # O valor é a data selecionada
        print(f'Data selecionada: {value}')

MainApp().run()
