from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener

Builder.load_file('widgets/pyles_list.kv')

class PylesList(BoxLayout, KeyboardListener):
    tabs = ObjectProperty(None)
     
    def __init__(self, **kwargs):
        super(PylesList, self).__init__(**kwargs)
        #self.app = App.get_running_app()
        #print(self.app)
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        return True