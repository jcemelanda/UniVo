"""
UniVo is a AAC system completely free and open source to provide people wotj tools to inclusive communication
"""
from toga.style.pack import COLUMN, ROW, Pack
from toga.constants import WindowState
from univo.db import get_categories, get_pictograms
import os
import toga
from univo.services import get_services

class UniVo(toga.App):
    def startup(self):
        main_box = toga.Box(direction=COLUMN, style=Pack(margin=10))

        # Botões fixos "Sim" e "Não" no topo
        self.pictogram_dir = os.path.join(os.path.dirname(__file__), "resources/pictograms")
        # platform services (tts, clipboard, storage)
        self.services = get_services()
        yes_no_box = toga.Box(
            direction=ROW,
            flex=1,
            style=Pack(margin_bottom=10))
        yes_btn = toga.Button(
            id="yes",
            flex=1, 
            icon=os.path.abspath(os.path.join(self.pictogram_dir, "base/yes.png")), 
            style=Pack(width=100, margin_right=10), 
            on_press=self.add_word)
        no_btn = toga.Button(
            id='no',
            flex=1,  
            icon=os.path.abspath(os.path.join(self.pictogram_dir, "base/no.png")), 
            style=Pack(width=100), 
            on_press=self.add_word)
        yes_no_box.add(yes_btn)
        yes_no_box.add(no_btn)
        main_box.add(yes_no_box)

        # Painel de frase construída
        self.phrase_label = toga.Label("Sentence:", style=Pack(font_size=16, margin_bottom=10))
        self.phrase_box = toga.Box(direction=ROW, flex=1, style=Pack(margin_bottom=10))
        main_box.add(self.phrase_label)
        main_box.add(self.phrase_box)

        # Categorias
        categories = get_categories()
        category_box = toga.Box(direction=ROW, flex=2, style=Pack(margin_bottom=10))
        for cat in categories:
            icon_path = os.path.abspath(os.path.join(self.pictogram_dir, f"{cat}/{cat}.png"))
            btn = toga.Button(
                id=cat, 
                flex=1, 
                icon=icon_path, 
                on_press=self.show_category)
            category_box.add(btn)
        main_box.add(category_box)

        # Área de símbolos/frases
        self.symbols_box = toga.Box(direction=ROW, flex=2, style=Pack(margin_bottom=10))
        main_box.add(self.symbols_box)

        # Botão para falar a frase
        speak_btn = toga.Button(
            id="speak", 
            flex=1,
            icon=os.path.abspath(os.path.join(self.pictogram_dir, "base/speaker.png")), 
            on_press=self.speak_phrase)
        main_box.add(speak_btn)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        self.main_window.state = WindowState.MAXIMIZED

    def add_word(self, widget):
        lbl = toga.Label(widget.id+' ')
        self.phrase_box.add(lbl)

    def show_category(self, widget):
        self.symbols_box.children.clear()

        items = get_pictograms(widget.id)

        for id_, icon_file in items:
            icon_path = os.path.abspath(os.path.join(self.pictogram_dir, widget.id, icon_file))
            btn = toga.Button(
                id=id_,
                flex=1, 
                icon=icon_path,
                on_press=self.add_word,
                style=Pack(margin_right=5)
            )
            self.symbols_box.add(btn)

    def speak_phrase(self, widget):
        # build phrase and use platform TTS
        phrase = " ".join([c.text for c in self.phrase_box.children])
        try:
            self.services.tts.speak(phrase)
        except Exception:
            # fallback: show dialog
            toga.InfoDialog("Falar", phrase).show()

def main():
    return UniVo(icon='resources/icon.png')