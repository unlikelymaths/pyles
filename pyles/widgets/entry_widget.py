from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener
from data.entry import Entry, EntryException
from linktypes import linktype_manager
from widgets.common import SingleLabel

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/entry_widget.kv'))


class EntryWidget(BoxLayout):
    entry = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.ids.image_widget.load_entry(self.entry)
        
    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            self.app.set_widget('edit', self.entry)
            return True