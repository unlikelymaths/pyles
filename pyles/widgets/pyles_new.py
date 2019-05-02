from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener
from linktypes import linktypes
from widgets.common import SingleLabel, SingleTextinput

Builder.load_file('widgets/pyles_new.kv')


class PylesNew(BoxLayout):

    def __init__(self, **kwargs):
        super(PylesNew, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.on_linktype(self.ids.linktype_selection.text)
        
    
    def on_back_button(self):
        self.app.set_widget('list')
        
    def on_linktype(self, linktype): 
        linktype = linktypes.all[linktype]
        grid_layout = self.ids.linktype_settings
        
        grid_layout.clear_widgets()
        if hasattr(linktype, 'settings'):
            for setting in linktype.settings:
                grid_layout.add_widget(SingleLabel(text=setting.name))
                grid_layout.add_widget(SingleTextinput())