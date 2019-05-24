from kivy.app import App

from widgets.common import DropManager
from widgets.pyles_list import PylesList
from widgets.pyles_edit import PylesEdit
from widgets.util import widget_path
from widgets.card_widget import CardWidget
from widgets.status_bar import status

from data.entry import get_entry_list

class Pyles(App,DropManager):

    def on_start(self):
        self.load_entries()
        self.set_widget('list')

    def load_entries(self):
        status.message('Loading entries', weak=True)
        self.entry_list = get_entry_list()
        num_entries = len(self.entry_list)
        if num_entries == 1:
            text = 'Loaded 1 entry'
        else:
            text = 'Loaded {} entries'.format(num_entries)
        status.message(text)

    def set_widget(self, widget_name, entry=None):
        self.root.content.clear_widgets()
        if widget_name == 'list':
            self.root.content.add_widget(PylesList())
        elif widget_name == 'new':
            self.root.content.add_widget(PylesEdit())
        elif widget_name == 'edit':
            self.root.content.add_widget(PylesEdit(entry))