import weakref
import importlib
from widgets.common import FilePathTextInput, SpinnerInput
 
class GenericSetting():
    def __init__(self, key, label, **kwargs):
        self.key = key
        self.label = label
        self.widget = None
        
    def serialize(self):
        return {'__name__': self.__class__.__name__,
                '__module__': self.__class__.__module__,
                'key': self.key, 'label': self.label}
                
    def apply(self):
        pass

def get_setting(config, key):
    settings = [setting for setting in config if setting.key == key]
    if len(settings) == 0:
        raise KeyError('Invalid config setting "{}"'.format(key))
    return settings[0]
    
class FilePathSetting(GenericSetting):
    def __init__(self, key, label, **kwargs):
        super().__init__(key, label, **kwargs)
        self._value = kwargs.get('value', '')
        
    def get_widget(self, callback = None):
        widget = FilePathTextInput(text = self._value)
        self.widget = weakref.proxy(widget)
        if callback is not None:
            self.widget.bind(text=callback)
        return widget
        
    def serialize(self):
        return {**super().serialize(),
            'value': self.value}
            
    def apply(self):
        self._value = self.value
        
    def has_changed(self):
        return self._value != self.value
        
    @property
    def value(self):
        if self.widget is not None:
            return self.widget.text
        return self._value
        
class MultipleChoiceSetting(GenericSetting):
    def __init__(self, key, label, options, **kwargs):
        super().__init__(key, label, **kwargs)
        self._value = kwargs.get('value', options[0])
        self._options = options
        
    def get_widget(self, callback = None):
        widget = SpinnerInput(text = self._value,
            values = self._options)
        self.widget = weakref.proxy(widget)
        if callback is not None:
            self.widget.bind(text=callback)
        return widget
        
    def serialize(self):
        return {**super().serialize(),
            'value': self.value,
            'options': self._options}
            
    def apply(self):
        self._value = self.value
        
    def has_changed(self):
        return self._value != self.value
        
    @property
    def value(self):
        if self.widget is not None:
            return self.widget.text
        return self._value