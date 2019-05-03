import weakref
from widgets.common import FilePathTextInput
 
class GenericSetting():
    def __init__(self, name = ''):
        self.name = name
        self.widget = None


        
class FilePathSetting(GenericSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_widget(self):
        widget = FilePathTextInput()
        self.widget = weakref.proxy(widget)
        return widget
        
    def get_value(self):
        if self.widget is not None:
            return self.widget.text
        return None