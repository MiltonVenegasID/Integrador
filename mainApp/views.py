from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from chatterbot import ChatBot
from smtplib import  SMTP
from django.http import JsonResponse, HttpResponse
import pyttsx3
from .AdaptadoresLogicos import *
import wikipedia
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import threading
from django.shortcuts import render, redirect
from nltk.sentiment.util import *
import nltk
import speech_recognition as sr

nltk.download('vader_lexicon')
stemmer = SnowballStemmer("spanish")
lemmatizer = WordNetLemmatizer()
wikipedia.set_lang('es')
engine = pyttsx3.init()
r = sr.Recognizer()


# Create your views here.
class Inicio(View):
    def get(self, request):
        return render(request, 'Heros.html')
    
class CustomChatBot(ChatBot):
    def get_response(self, input_statement, **kwargs):
        request = kwargs.get('request', None)
        for adapter in self.logic_adapters:
            if hasattr(adapter, 'set_request'):
                adapter.set_request(request)
        return super().get_response(input_statement, **kwargs)

chatbot = CustomChatBot('Heros', 
storage_adapters = [
        {'import_path': 'chatterbot.storage.ContextualMemoryStorageAdapter'}
    ],
    comparison_method= [ 
    { 'import_path': 'chatterbot.comparisons.LevenshteinDistance' }
], response_selection = [
    { 'import_path': 'chatterbot.response_selection.get_first_response' },
],     
    logic_adapters=[
    {
        'import_path': 'chatterbot.logic.BestMatch',
    },
    { 'import_path': 'mainApp.AdaptadoresLogicos.JustinTeAmo'}
])

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.engine.getProperty('rate') * 0.8)
        self.engine.setProperty('volume', 1.0)

    def speak(self, text):
        if not self.engine.isBusy():
            self.engine.say(str(text))
            self.engine.runAndWait()
            
    def speak_in_thread(self, text):
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.start()
        #TODO:
        #FIXME:

tts = TextToSpeech()
    
def fetch_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Tu peticion podria incluir demasiados temas {e.options}"
    except wikipedia.exceptions.PageError:
        return "No pude encontrar información sobre ese tema"
    
def preprocess_text(text):
    tokens = word_tokenize(text, language='spanish')
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.lower() ]
    JoinTokens =  ' '.join(lemmatized_tokens)
    preprocessed_text = JoinTokens
    return preprocessed_text
    
def show_spinner(request):
    return JsonResponse({'show_spinner': True})

def hide_spinner(request):
    return JsonResponse({'show_spinner': False})

def get_bot_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        preprocessed_input = preprocess_text(user_input)

        if any(keyword in user_input.lower() for keyword in ["investiga", "busca", "búscame", "busca sobre", "investigame", "buscame"]):
            topic = user_input.lower().replace("investiga", "").replace("busca", "").replace("búscame", "").replace("busca sobre", "").strip()
            bot_response = fetch_wikipedia_summary(topic)

        else:
            chatterbot_response = chatbot.get_response(preprocessed_input, request=request)
            bot_response = chatterbot_response.text

        response = JsonResponse({'response': str(bot_response)})
        threading.Thread(target=tts.speak, args=(bot_response,)).start()

        return response

    return JsonResponse({'response': 'Solicitud inválida'}, status=400)