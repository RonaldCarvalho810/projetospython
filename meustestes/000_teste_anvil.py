# from ._anvil_designer import Form1Template
# from anvil import *
# from anvil import Notification

# class Form1(Form1Template):
#     def __init__(self, **properties):
#         # Inicializa as propriedades e associações de dados do formulário
#         self.init_components(**properties)

#     def button_1_click(self, **event_args):
#         """Este método é chamado quando o botão é clicado"""
#         # Obtém o valor da data selecionada no DatePicker
#         dia = self.date_picker_1.date
        
#         # Verifica se o usuário selecionou uma data
#         if dia:
#             Notification(f"Teste bem sucedido, dia {dia}").show()  # Exibe a notificação
#             print(f"Teste bem sucedido, dia {dia}")  # Imprime no console
#         else:
#             Notification("Por favor, selecione uma data.").show()
#             print("Nenhuma data selecionada")
