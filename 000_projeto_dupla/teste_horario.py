from kivymd.app import MDApp

try:
    from kivymd.uix.pickers import MDTimePicker  # versão antiga
except:
    from kivymd.uix.pickers import MDTimePicker  # versão nova


class MainApp(MDApp):
    def build(self):
        return

    def on_start(self):
        time_picker = MDTimePicker()
        time_picker.bind(time=self.hora_selecionada)
        time_picker.open()

    def hora_selecionada(self, instance, time):
        print(f'Horário selecionado: {time}')


MainApp().run()
