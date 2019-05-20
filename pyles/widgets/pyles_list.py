from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener

from widgets.util import widget_path
from widgets.entry_widget import EntryWidget

Builder.load_file(widget_path('widgets/pyles_list.kv'))

class PylesList(BoxLayout, KeyboardListener):
    tabs = ObjectProperty(None)
     
    def __init__(self, **kwargs):
        super(PylesList, self).__init__(**kwargs)
        # Set the height in order to allow scrolling
        self.ids.entry_widget.bind(minimum_height=self.ids.entry_widget.setter('height'))
        # Get the app
        self.entry_list = App.get_running_app().entry_list
        self.entry_list.add_callback(self.reload_list)
        self.reload_list(self.entry_list)
        
    def reload_list(self, entry_list):
        self.ids.entry_widget.clear_widgets()
        for entry in entry_list.entries:
            l = EntryWidget(entry=entry)
            self.ids.entry_widget.add_widget(l)
        
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        return True