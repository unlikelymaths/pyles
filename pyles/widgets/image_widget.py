from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from widgets.common import DropWidget
from data.icon import Icon, from_file, IconLoadError

from widgets.util import widget_path
from widgets.loading_widget import LoadingWidget


Builder.load_file(widget_path('widgets/image_widget.kv'))

class ImageWidget(DropWidget):
    icon = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.layout_callback)
        self.bind(pos=self.layout_callback)
        
    def layout_callback(self, instance, value):
        self.draw()
            
    def draw(self):
        if self.icon is not None:
            if self.icon.state == Icon.READY:
                self.canvas.clear()
                with self.canvas:
                    self.icon.draw(self.pos, self.size)
        else:
            self.canvas.clear()
    
    def on_state(self, icon, state):
        if state == Icon.EMPTY:
            self.clear_widgets()
        elif state == Icon.LOADING:
            pass
        elif state == Icon.FAILED:
            self.clear_widgets()
            self.icon = None
        elif state == Icon.READY:
            self.clear_widgets()
        self.draw()
            
    def load_entry(self, entry):
        self.canvas.clear()
        self.clear_widgets()
        self.icon = entry.icon
        if self.icon.state == Icon.READY:
            self.on_state(self.icon, self.icon.state)
        else:
            self.icon.bind(state=self.on_state)
            self.add_widget(LoadingWidget())
    
    def load_file(self, file_path):
        self.canvas.clear()
        self.clear_widgets()
        self.icon = from_file(file_path)
        self.icon.bind(state=self.on_state)
        self.add_widget(LoadingWidget())
    
    def drop(self, file_path):
        self.load_file(file_path)
        return True