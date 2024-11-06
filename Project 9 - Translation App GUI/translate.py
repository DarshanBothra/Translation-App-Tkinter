# Libraries Used
'''
customtkinter
googletrans==3.1.0a0 (pip3 install)
pillow (pip3 install)
CustomTkinterMessagebox (pip3 install)
gTTS (pip3 install)
playsound (pip3 install)
SpeechRecognition


NOTE: 
1. legacy-cgi (pip3 install). cgi is one of the internal modules used which was discontinued in python 3.13 instead legacy-cgi is used as extended support for the original cgi
2. PyObjC (pip3 install) - subpackage to run playsound efficiently
3. install standard-aifc for speech recognition (sub package)
4. install PyAudio (subpackage for speech recognition)
'''

from customtkinter import *
import googletrans
from PIL import Image
from CustomTkinterMessagebox import CTkMessagebox
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from time import sleep
import os

# Set up a translator
translator = googletrans.Translator()

# Set up a speech recognizer
recognizer = sr.Recognizer()

# Functions
def playOutput():
    bottom_label.configure(text = "")
    # Change Button Color
    speaker_output_button.configure(fg_color = "#d1d1d1")

    # Get the Translated Text
    translated_text = translated_text_box.get("0.0", "end")

    # If there is some text 
    try:
        # Covnert Text to Speech and Save the File
        translated_speech = gTTS(translated_text)
        translated_speech.save("translation.mp3")

        # Play the file using playsound
        playsound("translation.mp3")

    # If there is no text
    except Exception as e:
        message_box = CTkMessagebox.messagebox(title = "Translator", text = e, sound = "off", center = False, top = False)

def listenInput():
    bottom_label.configure(text = "")

    speak_input_button.configure(fg_color = "#d1d1d1")

    with sr.Microphone() as source:
        
        try:
            # Obrain voice input from the microphone
            recognizer.adjust_for_ambient_noise(source)
            audio_text = recognizer.listen(source, timeout = 2)

            # bottom_label.configure(text = "")
            # Convert and obtain the speech in string form
            original_text = recognizer.recognize_google(audio_text)

            # Display it in the orginal text box and call translate
            original_text_box.delete("0.0", "end")
            original_text_box.insert("0.0", original_text)
            translated_text_box.configure(state = "normal")
            translated_text_box.delete("0.0", "end")
            translated_text_box.configure(state = "disabled")
            translateText()

        except:

            # Display and play a sound for the sorry message

            bottom_label.configure(text = "Sorry! Couldn't get you")
            translated_message = gTTS("Sorry! Couldn't get you.")
            translated_message.save("sorry message.mp3")
            playsound("sorry message.mp3")
    speak_input_button.configure(fg_color = "#e3e3e3")

            
def switchLangs():
    # Extracting the From and To Languages and switching them
    bottom_label.configure(text = "")

    from_lang = original_combo.get().lower()
    for key, value in languages.items():
        if value == from_lang:
            from_lang_key = key

    to_lang = translated_combo.get().lower()
    for key, value in languages.items():
        if value == to_lang:
            to_lang_key = key
    
    # Switching the two languages
    from_lang, to_lang = to_lang, from_lang
    from_lang_key, to_lang_key = to_lang_key, from_lang_key

    # Setting the values in the combo-box
    original_combo.set(from_lang.capitalize())
    translated_combo.set(to_lang.capitalize())

    # Obtaining the translated text to be put as original text

    # Deleting the stuff in the original text box
    original_text_box.delete("0.0", "end")

    # Geting the old stuff and deleting the stuff in translated text box
    translated_text_box.configure(state = "normal")
    text = translated_text_box.get("0.0", "end")
    translated_text_box.delete("0.0", "end")
    translated_text_box.configure(state = "disabled")

    # Settings the translated text as original text 
    original_text_box.insert("0.0", text)

    # Calling the Translation function
    translateText()

def translateText():
    bottom_label.configure(text = "")

    # Change the color of the microphone button if it was used
    speak_input_button.configure(fg_color = "#e3e3e3")

    # Get the languages from the dictionary-keys

    # Get the From Language-key
    from_language = original_combo.get().lower()
    
    for lang in languages:
        if languages[lang] == from_language:
            from_language_key = lang

    # Get the To Language-key
    to_language = translated_combo.get().lower()
    
    for lang in languages:
        if languages[lang] == to_language:
            to_language_key = lang

    # Translation

    original = original_text_box.get("0.0", "end")

    translated = translator.translate(original, dest = to_language_key)

    global translated_pronunciation
    translated_pronunciation = translated.pronunciation
    translated_text = translated.text

    
    # Output the translated text on the translated box

    translated_text_box.configure(state = "normal")
    translated_text_box.delete("0.0", "end")
    translated_text_box.insert("0.0", translated_text)
    translated_text_box.configure(state = "disabled")


def clearText():
    bottom_label.configure(text = "")

    '''
    This clears the both the text boxes from start to end
    '''
    original_text_box.delete("0.0", "end")

    translated_text_box.configure(state = "normal")
    translated_text_box.delete("0.0", 'end')
    translated_text_box.configure(state = "disabled")

# Main Window
root = CTk()
root.geometry("890x330")
root.title('Translator')
set_appearance_mode("light")
root.configure(fg_color = "#ffffff")

# Text boxes

# Original Text Box - Both ead and Write
original_text_box = CTkTextbox(master = root, height = 200, width = 350, font = ("Halvetica", 16), corner_radius= 20, fg_color= '#ffffff', text_color="#343434", wrap = "word", border_color = "#646464", border_width=1)
original_text_box.grid(row = 0, column = 0, pady = 20, padx = 10, rowspan = 3)

# Translated Text Box - Read Only
translated_text_box = CTkTextbox(master = root, height = 200, width = 350, font = ("Halvetica", 16), corner_radius= 20, fg_color= '#ffffff', text_color="#343434", wrap = "word", border_color = "#646464", border_width=1, state = "disabled")
translated_text_box.grid(row = 0, column = 3, pady = 20, padx = 10, rowspan = 3)

# Buttons

# Translate Button
translate_button = CTkButton(master = root, text = "Translate", font = ("Halvetica", 20), command = translateText, height = 40, corner_radius = 6, fg_color = "#e3e3e3", text_color= "#646464", hover_color = "#d1d1d1")
translate_button.grid(row = 0, column = 1, columnspan = 2, padx = 5, sticky = "s")

# Switch Language Button
switch = CTkImage(Image.open("switch.png"), size = (30, 30))
switch_button = CTkButton(master = root, image = switch, text = "", height = 40, corner_radius = 6, fg_color="#e3e3e3", hover_color = "#d1d1d1", command = switchLangs)
switch_button.grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 20)

# Clear Button
clear_button = CTkButton(master = root, text = "Clear", font = ("Halvetica", 20), command = clearText, height = 40, corner_radius = 6, fg_color = "#e3e3e3", text_color= "#646464", hover_color = "#d1d1d1")
clear_button.grid(row = 2, column = 1, columnspan = 2, padx = 5, sticky = "n")

# Speak - Input
mic = CTkImage(Image.open("microphone.png"), size = (20, 20))
speak_input_button = CTkButton(master = root, image = mic, text = "", width = 50, height = 50, fg_color="#e3e3e3", hover_color = "#d1d1d1", command = listenInput)
speak_input_button.grid(row = 3, column = 1)

# Speaker - Output
speaker = CTkImage(Image.open("speaker.png"), size = (35, 35))
speaker_output_button = CTkButton(master = root, image = speaker, text = "", width = 50, height = 50, fg_color="#e3e3e3", hover_color = "#d1d1d1", command = playOutput)
speaker_output_button.grid(row = 3, column = 2)

# Combo Boxes

languages = googletrans.LANGUAGES
language_list = []
for item in languages.items():
    language_list.append(item[1].capitalize())


# Original ComboBox
original_combo = CTkComboBox(master = root, width = 350, height = 40, corner_radius = 2.5, border_width = 0, fg_color = "#e3e3e3", dropdown_fg_color = "#e3e3e3", dropdown_text_color = "#646464", text_color = "#646464", font = ("Halvetica", 16), values = language_list, button_color="#e3e3e3", justify = 'center')
original_combo.set("English")
original_combo.grid(row = 3, column = 0)

# Tanslated ComboBox
translated_combo = CTkComboBox(master = root, width = 350, height = 40, corner_radius = 2.5, border_width = 0, fg_color = "#e3e3e3", dropdown_fg_color = "#e3e3e3", dropdown_text_color = "#646464", text_color = "#646464", font = ("Halvetica", 16), values = language_list, button_color="#e3e3e3", justify = 'center')
translated_combo.set("Hindi")
translated_combo.grid(row = 3, column = 3)

# Bottom Label
bottom_label = CTkLabel(master = root, text = "", height = 20, font = ("Halvetica", 15), text_color = "#646464")
bottom_label.grid(row = 4, column = 0, columnspan = 4, sticky = 's', pady = 10)

root.mainloop()

# Check if the file translation.mp3 exits in the directory, if yes, then remove it

directory_list = os.listdir()
for item in directory_list:
    if item == "translation.mp3" or item == "sorry message.mp3":
        os.remove(item)