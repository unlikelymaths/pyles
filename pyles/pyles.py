from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty

from kivy.uix.gridlayout  import GridLayout
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import data
from util import KeyboardListener
from widgets.pyles_list import PylesList
from widgets.pyles_new import PylesNew

import linktypes.linktypes as linktypes

class Pyles(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.drops = []
        Window.bind(on_dropfile=self.on_dropfile)
    
    def on_start(self):
        self.settings = data.load_settings()
        data.save_settings(self.settings)
        print(self.settings)
        self.set_widget('list')
       
    def on_dropfile(self, widget, file_path):
        mouse_pos = Window.mouse_pos
        print(mouse_pos)
        #for func in self.drops:
        #    if func(widget, file_path, mouse_pos):
        #        return
        
    def set_widget(self, widget_name):
        self.root.clear_widgets()
        if widget_name == 'list':
            self.root.add_widget(PylesList())
        elif widget_name == 'new':
            self.root.add_widget(PylesNew())
    
if __name__ == '__main__':
    Pyles().run()