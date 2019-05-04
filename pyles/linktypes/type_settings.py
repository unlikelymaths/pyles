import weakref
from widgets.common import FilePathTextInput
 
class GenericSetting():
    def __init__(self, key, label = ''):
        self.key = key
        self.label = label
        self.widget = None
        
class FilePathSetting(GenericSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_widget(self):
        widget = FilePathTextInput()
        self.widget = weakref.proxy(widget)
        return widget
        
    @property
    def value(self):
        if self.widget is not None:
            return self.widget.text
        return None