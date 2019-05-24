from kivy.uix.boxlayout  import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/status_bar.kv'))

class StatusBar(BoxLayout):
    DEFAULT_COLOR = [1,1,1,1]
    ERROR_COLOR = [1,0.2,0.2,1]
    
    status = StringProperty('')
    color = ListProperty(DEFAULT_COLOR)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)