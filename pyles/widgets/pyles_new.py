from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener

Builder.load_file('widgets/pyles_new.kv')


class PylesNew(BoxLayout):

    def __init__(self, **kwargs):
        super(PylesNew, self).__init__(**kwargs)
        self.app = App.get_running_app()
    
    def on_back_button(self):
        self.app.set_widget('list')