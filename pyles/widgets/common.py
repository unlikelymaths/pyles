from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.lang import Builder

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/common.kv'))

class SingleLabel(Label):
    pass
    
class SingleTextinput(TextInput):
    pass
    
class SingleSpinner(Spinner):
    pass
    
class TreeAgnosticWidget(Widget):
    """Provides callback on_tree when widget is added/removed from tree"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(parent=self._ancestors_callback)
        self._is_in_tree = None
        self._ancestors = []

    def _ancestors_callback(self, instance, value):
        for ancestor in self._ancestors:
            try:
                ancestor.unbind(parent=self._ancestors_callback)
            except ReferenceError:
                pass
        ancestor = self.parent
        while isinstance(ancestor,Widget):
            ancestor_ref = ancestor.proxy_ref
            self._ancestors.append(ancestor_ref)
            ancestor_ref.bind(parent=self._ancestors_callback)
            ancestor = ancestor.parent
            
        if ancestor is None:
            if self._is_in_tree != False:
                self.on_tree(False)
            self._is_in_tree = False
        else:
            if self._is_in_tree != True:
                self.on_tree(True)
            self._is_in_tree = True
        
    def on_tree(self, is_in_tree):
        pass 
    
class DropManager():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._drop_widgets = []
        Window.bind(on_dropfile=self.on_dropfile)
            
    def add_drop_widget(self, drop_widget):
        self._drop_widgets.append(drop_widget)
    
    def remove_drop_widget(self, drop_widget):
        if drop_widget in self._drop_widgets:
            self._drop_widgets.remove(drop_widget)
        
    def on_dropfile(self, widget, file_path):
        file_path = file_path.decode('utf8')
        invalid_drop_widgets = []
        for drop_widget in self._drop_widgets:
            try:
                if drop_widget.check_drop(file_path, Window.mouse_pos):
                    return
            except ReferenceError:
                invalid_drop_widgets.append(drop_widget)
        for drop_widget in invalid_drop_widgets:
            self.remove_drop_widget(drop_widget)
        
class DropWidget(TreeAgnosticWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = App.get_running_app()

    def on_tree(self, is_in_tree):
        if is_in_tree:
            self.app.add_drop_widget(self.proxy_ref)
        else:
            self.app.remove_drop_widget(self.proxy_ref)
        
    def check_drop(self, file_path, mouse_pos):
        mouse_pos = self.to_widget(*mouse_pos)
        if self.collide_point(*mouse_pos):
            return self.drop(file_path)
        return False
        
    def drop(self, file_path):
        pass
        
        
class FilePathTextInput(SingleTextinput, DropWidget):
    def drop(self, file_path):
        self.text = file_path