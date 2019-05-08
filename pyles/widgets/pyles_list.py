from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener
from data.entry import EntryList

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/pyles_list.kv'))

class PylesList(BoxLayout, KeyboardListener):
    tabs = ObjectProperty(None)
     
    def __init__(self, **kwargs):
        super(PylesList, self).__init__(**kwargs)
        self.entry_list = EntryList()
        #self.app = App.get_running_app()
        #print(self.app)
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        return True