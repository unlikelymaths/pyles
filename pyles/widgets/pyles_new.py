from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener
from data.entry import Entry, EntryException
from linktypes import linktypes
from widgets.common import SingleLabel

Builder.load_file('widgets/pyles_new.kv')


class PylesNew(BoxLayout):

    def __init__(self, **kwargs):
        super(PylesNew, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.entry = None
        self.on_linktypename(self.ids.linktype_selection.text)
        
    def on_back_button(self):
        self.app.set_widget('list')
        
    def on_save_button(self):
        linktypename = self.ids.linktype_selection.text
        kwargs = {'name': self.ids.name_input.text,
            'linktypename': linktypename,
            'imagesection': self.ids.image_widget.imagesection,
            'linktypeconfig': {
                setting.key: setting.value 
                for setting in linktypes.get_config(linktypename)}}
        
        try:
            self.entry = Entry(**kwargs)
        except EntryException as e:
            print(e)
                
    def on_linktypename(self, linktypename):
        self.ids.linktype_settings.clear_widgets()
        for setting in linktypes.get_config(linktypename):
            self.ids.linktype_settings.add_widget(SingleLabel(text=setting.label))
            self.ids.linktype_settings.add_widget(setting.get_widget())