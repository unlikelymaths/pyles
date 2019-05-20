import weakref
import importlib
from widgets.common import FilePathTextInput
 
class GenericSetting():
    def __init__(self, key, label = '', **kwargs):
        self.key = key
        self.label = label
        self.widget = None
        
    def serialize(self):
        return {'__name__': self.__class__.__name__,
                '__module__': self.__class__.__module__,
                'key': self.key}

def get_setting(config, key):
    settings = [setting for setting in config if setting.key == key]
    if len(settings) == 0:
        raise KeyError('Invalid config setting "{}"'.format(key))
    return settings[0]
    
class FilePathSetting(GenericSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = kwargs.get('value', '')
        
    def get_widget(self):
        widget = FilePathTextInput(text = self._value)
        self.widget = weakref.proxy(widget)
        return widget
        
    def serialize(self):
        return {**super().serialize(),
            'value': self.value}
        
    @property
    def value(self):
        if self.widget is not None:
            return self.widget.text
        return self._value