from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.lang import Builder

Builder.load_file('widgets/common.kv')

class SingleLabel(Label):
    pass

class SingleTextinput(TextInput):
    pass
    
class SingleSpinner(Spinner):
    pass
    
class DropManager():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._drop_widgets = []
        Window.bind(on_dropfile=self.on_dropfile)
            
    def add_drop_widget(self, drop_widget):
        self._drop_widgets.append(drop_widget)
    
    def remove_drop_widget(self, drop_widget):
        self._drop_widgets.remove(drop_widget)
        
    def on_dropfile(self, widget, file_path):
        for drop_widget in self._drop_widgets:
            if drop_widget.check_drop(file_path, Window.mouse_pos):
                return

class DropWidget(Widget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = App.get_running_app()
                
    def on_parent(self, widget, parent):
        if parent is None:
            self.app.remove_drop_widget(self.proxy_ref)
        else:
            self.app.add_drop_widget(self.proxy_ref)
        
    def check_drop(self, file_path, mouse_pos):
        if self.collide_point(*mouse_pos):
            return self.drop(file_path)
        return False
        
    def drop(self, file_path):
        pass