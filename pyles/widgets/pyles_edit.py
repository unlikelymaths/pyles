from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App

from util import KeyboardListener
from data.entry import Entry, EntryException
from linktypes import manager
from linktypes.settings import LinktypeException
from widgets.common import SingleLabel
from widgets.status_bar import status

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/pyles_edit.kv'))


class PylesEdit(BoxLayout):

    def __init__(self, entry = None, **kwargs):
        super(PylesEdit, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.linktypeconfig = None
        self.entry = entry
        if self.entry is None:
            self.on_linktypename(self.ids.linktype_selection.text)
        else:
            self.ids.linktype_selection.text = self.entry.linktype.name
            self.ids.name_input.text = self.entry.name
            self.ids.image_widget.load_entry(self.entry)
            self.linktypeconfig = self.entry.linktypeconfig
            self.build_settings()
    
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
            # LinkType has changed
            if self.linktypeconfig != self.entry.linktypeconfig:
                return True
            # Setting has changed
            for key, setting in self.linktypeconfig['settings'].items():
                if setting.has_changed():
                    return True
            # Icon has changed
            if self.ids.image_widget.icon != self.entry.icon:
                return True
        return False

    def on_back_button(self):
        self.app.set_widget('list')
        
    def on_save_button(self):
        if len(self.ids.name_input.text) == 0:
            status.message('Name must not be empty', weak=True)
            return
        if not self.has_changed():
            status.message('No changes to write', weak=True)
            return
        name = self.ids.name_input.text
        kwargs = {'icon': self.ids.image_widget.icon,
                  'linktypeconfig': self.linktypeconfig}
        if self.entry is None:
            status.message('Saving new entry {}'.format(name), weak=True)
            try:
                self.entry = Entry(name=name,**kwargs)
                status.message('Saved new entry {}'.format(name), weak=True)
            except (EntryException, LinktypeException) as e:
                status.error(e)
        elif self.entry.name != name:
            status.message('Saving entry {}'.format(name), weak=True)
            try:
                new_entry = Entry(name=name,**kwargs)
                if new_entry is not None:
                    self.entry.delete()
                    self.entry = new_entry
                status.message('Saved entry {}'.format(name), weak=True)
            except (EntryException, LinktypeException) as e:
                status.error(e)
        else:
            status.message('Saving entry {}'.format(name), weak=True)
            try:
                self.entry.save(**kwargs)
                status.message('Saved entry {}'.format(name), weak=True)
            except (EntryException, LinktypeException) as e:
                status.error(e)

    def on_linktypename(self, linktypename):
        self.linktypeconfig = manager.get_config(linktypename)
        self.build_settings()
        
    def build_settings(self):
        if self.linktypeconfig:
            self.ids.linktype_settings.clear_widgets()
            for key, setting in self.linktypeconfig['settings'].items():
                self.ids.linktype_settings.add_widget(
                    SingleLabel(text=setting.label))
                self.ids.linktype_settings.add_widget(
                    setting.get_widget())
            