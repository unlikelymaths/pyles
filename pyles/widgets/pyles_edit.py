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

Builder.load_file(widget_path('widgets/pyles_edit.kv'))


class PylesEdit(BoxLayout):

    def __init__(self, entry = None, **kwargs):
        super(PylesEdit, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.entry = entry
        if self.entry is None:
            self.on_linktypename(self.ids.linktype_selection.text)
        else:
            self.linktypeconfig = self.entry.linktypeconfig
            self.ids.name_input.text = self.entry.name
            self.ids.image_widget.load_entry(self.entry)
            self.build_settings()
        self._last_image_path = self.get_current_iamge_path()
        self.ids.name_input.bind(text=self.check_save_button)
        self.ids.image_widget.bind(image=self.check_save_button)
        self.check_save_button()
    
    def get_current_iamge_path(self):
        if self.ids.image_widget.image is not None:
            return self.ids.image_widget.image.filename
        return None
    
    def has_changed(self):
        # Not editing an entry
        if self.entry is None:
            # Name is mandatory
            if len(self.ids.name_input.text) > 0:
                return True
        else:
            # Name has changed
            if self.ids.name_input.text != self.entry.name:
                return True
            # Setting has changed
            for setting in self.linktypeconfig:
                if setting.has_changed():
                    return True
            # Image has changed
            if self._last_image_path != self.get_current_iamge_path():
                return True
        return False
    
    def check_save_button(self, *args, **kwargs):
        print('check_save_button')
        self.ids.save_button.disabled = not self.has_changed()
            
    def on_back_button(self):
        self.app.set_widget('list')
        
    def on_save_button(self):
        linktypename = self.ids.linktype_selection.text
        kwargs = {'name': self.ids.name_input.text,
            'linktypename': linktypename,
            'imagesection': self.ids.image_widget.imagesection,
            'linktypeconfig': self.linktypeconfig}
        
        try:
            self.entry = Entry(**kwargs)
        except EntryException as e:
            print(e)
                
    def on_linktypename(self, linktypename):
        self.linktypeconfig = linktype_manager.get_config(linktypename)
        self.build_settings()
        
    def build_settings(self):
        self.ids.linktype_settings.clear_widgets()
        for setting in self.linktypeconfig:
            self.ids.linktype_settings.add_widget(
                SingleLabel(text=setting.label))
            self.ids.linktype_settings.add_widget(
                setting.get_widget(self.check_save_button))
            