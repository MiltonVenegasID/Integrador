import pandas as pd
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import requests

class Saludos(LogicAdapter):
    def  __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        
    def can_process():
        words = ['Hola', 'Saludos', 'Hola']
        return any(word in statement.text.lower() for word in words)
    
    def process(input_statement, additional_response_selection_parameter = None, **kwargs):
        response_statement = "Hola, Mucho gusto, soy Heros"
        response_statement.confidence = 1
        return response_statement
        
class JustinTeAmo(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        
    def can_process(self, statement):
        words = ['Artisa famoso', 'Famoso', 'Guapo', 'Sexy', 'verga de 47 cm']
        return any(word in statement.text.lower() for word in words)
    
    def process(self, input_statement, additional_response_selection_parameter=None, **kwargs):
        response_text = "No has iniciado sesión."
        response_statement = Statement(text=response_text)
        response_statement.confidence = 1
        return response_statement