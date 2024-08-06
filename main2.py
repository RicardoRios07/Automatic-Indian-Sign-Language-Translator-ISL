import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk
import string
from easygui import buttonbox, enterbox
import os
import re

isl_gif = [
    'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
    'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
    'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
    'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
    'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 
    'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
    'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
    'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
    'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
    'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
    'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
    'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
    'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahemdabad', 'all', 'april', 'assam', 'august', 
    'australia', 'badoda', 'banana', 'banaras', 'banglore', 'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 
    'church', 'clinic', 'coconut', 'crocodile', 'dasara', 'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 
    'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello', 'hindu', 'hyderabad', 'india', 'january', 'jesus', 
    'job', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango', 'may', 'mile', 'monday', 'mumbai', 'museum', 
    'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station', 'post office', 'pune', 'punjab', 
    'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica', 'story', 'sunday', 
    'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village', 
    'voice', 'wednesday', 'weight', 'please wait for sometime', 'what is your mobile number', 'what are you doing', 'are you busy',
    'hola', 'adiós', 'por favor', 'gracias', 'perdón', 'buenos días', 'buenas tardes', 'buenas noches', 
    'sí', 'no', 'cómo estás', 'bien', 'mal', 'qué hora es', 'dónde está el baño', 'cuánto cuesta', 
    'ayuda', 'comida', 'agua', 'música', 'teléfono', 'trabajo', 'estudio', 'familia', 'amigo', 'vacaciones'
]

def clean_phrase(phrase):
    cleaned_phrase = re.sub(r'\W+', '', phrase.lower())
    return cleaned_phrase

def show_sign_language(text):
    cleaned_phrase = clean_phrase(text)
    file_path = f'ISL_Gifs/{cleaned_phrase}.gif'
    
    if os.path.exists(file_path):
        class ImageLabel(tk.Label):
            """Una etiqueta que muestra imágenes y reproduce GIFs"""
            def load(self, im):
                if isinstance(im, str):
                    im = Image.open(im)
                self.loc = 0
                self.frames = []

                try:
                    for i in count(1):
                        self.frames.append(ImageTk.PhotoImage(im.copy()))
                        im.seek(i)
                except EOFError:
                    pass

                try:
                    self.delay = im.info['duration']
                except:
                    self.delay = 100

                if len(self.frames) == 1:
                    self.config(image=self.frames[0])
                else:
                    self.next_frame()

            def next_frame(self):
                if self.frames:
                    self.loc += 1
                    self.loc %= len(self.frames)
                    self.config(image=self.frames[self.loc])
                    self.after(self.delay, self.next_frame)
        
        root = tk.Tk()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(file_path)
        root.mainloop()
    else:
        print(f"El archivo {file_path} no se encontró.")
        for char in cleaned_phrase:
            if char in 'abcdefghijklmnopqrstuvwxyz':
                ImageAddress = f'letters/{char}.jpg'
                ImageItself = Image.open(ImageAddress)
                ImageNumpyFormat = np.asarray(ImageItself)
                plt.imshow(ImageNumpyFormat)
                plt.draw()
                plt.pause(0.8)
        plt.close()

def func():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Escuchando")
        audio = r.listen(source)
        try:
            a = r.recognize_google(audio, language='es-ES') or r.recognize_google(audio, language='en-US')
            a = a.lower()
            print('Usted dijo: ' + a)
            a = a.translate(str.maketrans('', '', string.punctuation))
            show_sign_language(a)
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"No se pudo solicitar resultados; {e}")

while True:
    image = "signlang.png"
    msg = "ESCUCHAR Y VER LENGUAJE DE SEÑAS"
    choices = ["Voz en Vivo", "Escribir Texto", "Salir"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == "Voz en Vivo":
        func()
    elif reply == "Escribir Texto":
        text_input = enterbox("Escribe el texto para traducir a lenguaje de señas:")
        if text_input:
            show_sign_language(text_input)
    elif reply == "Salir":
        break