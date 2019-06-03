import weakref
from widgets.common import FilePathTextInput, SpinnerInput

class LinktypeException(Exception):
    pass

class GenericSetting():
    def __init__(self, label, **kwargs):
        self.label = label
        self.widget = None

    def apply(self):
        pass

class FilePathSetting(GenericSetting):
    def __init__(self, label, **kwargs):
        super().__init__(label, **kwargs)
        self._path = kwargs.get('path', '')
        
    def get_widget(self, callback = None):
        widget = FilePathTextInput(text = self._path)
        self.widget = weakref.proxy(widget)
        if callback is not None:
            self.widget.bind(text=callback)
        return widget
        
    def serialize(self):
        return {'path': self.path}
            
    def apply(self):
        self._path = self.path
        
    def has_changed(self):
        return self._path != self.path
        
    @property
    def path(self):
        if self.widget is not None:
            return self.widget.text
        return self._path
        
class MultipleChoiceSetting(GenericSetting):
    def __init__(self, label, options, **kwargs):
        super().__init__(label, **kwargs)
        self._selection = kwargs.get('selection', options[0])
        self._options = options
        
    def get_widget(self, callback = None):
        widget = SpinnerInput(text = self._selection,
            values = self._options)
        self.widget = weakref.proxy(widget)
        if callback is not None:
            self.widget.bind(text=callback)
        return widget
        
    def serialize(self):
        return {'selection': self.selection}
            
    def apply(self):
        self._selection = self.selection
        
    def has_changed(self):
        return self._selection != self.selection
        
    @property
    def selection(self):
        if self.widget is not None:
            return self.widget.text
        return self._selection