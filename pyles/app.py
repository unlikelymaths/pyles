from kivy.app import App

from widgets.common import DropManager
from widgets.pyles_list import PylesList
from widgets.pyles_edit import PylesEdit
from widgets.util import widget_path
from widgets.card_widget import CardWidget

from data.entry import get_entry_list

class Pyles(App,DropManager):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry_list = get_entry_list()
    
    def on_start(self):
        self.set_widget('list')

    def set_widget(self, widget_name, entry=None):
        self.root.clear_widgets()
        if widget_name == 'list':
            self.root.add_widget(PylesList())
        elif widget_name == 'new':
            self.root.add_widget(PylesEdit())
        elif widget_name == 'edit':
            self.root.add_widget(PylesEdit(entry))