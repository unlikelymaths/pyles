from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.app import App


Builder.load_file('widgets/settings_widget.kv')


class SettingsWidget(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
    