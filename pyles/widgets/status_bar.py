import inspect
from collections import namedtuple
from kivy.uix.boxlayout  import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/status_bar.kv'))

DEFAULT_COLOR = [1,1,1,1]
ERROR_COLOR = [1,0.2,0.2,1]

Message = namedtuple('Message', ['text','duration','type','weak'])

def get_caller():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    return mod.__name__

class StatusManager():
    DEFAULT_INFO_DURATION = 5

    def __init__(self):
        self.bar = None
        self.current_message = None
        self.current_timer = None
        self.error_stack = []
        self.message_stack = []

    def message(self, text, duration = DEFAULT_INFO_DURATION, weak = False):
        Logger.info('{}: {}'.format(get_caller(), text))
        self.message_stack.append(Message(
            text = text,
            duration = duration,
            type = 'message',
            weak = weak))
        self._update()

    def _show_current_message(self):
        if self.bar:
            if self.current_message is not None:
                self.bar.status = self.current_message.text
                if self.current_message.type == 'message':
                    self.bar.color = DEFAULT_COLOR
                else:
                    self.bar.color = ERROR_COLOR
            else:
                self.bar.status = ''
                self.bar.color = DEFAULT_COLOR

    def _set_current_message(self, message):
        self.current_message = message
        self.current_timer = Clock.schedule_once(
            lambda dt: self._timeout(), message.duration)

    def _timeout(self):
        self.current_message = None
        self.current_timer = None
        self._update()

    def _prune_weak(self):
        if self.current_message is not None and self.current_message.weak:
            if self.current_timer is not None:
                self.current_timer.cancel()
            self.current_message = None
            self.current_timer = None

    def _update(self):
        self._prune_weak()
        if self.current_message is None:
            if len(self.error_stack) > 0:
                self._set_current_message(self.error_stack.pop(0))
            elif len(self.message_stack) > 0:
                self._set_current_message(self.message_stack.pop(0))
        self._show_current_message()

status = StatusManager()

class StatusBar(BoxLayout):
    status = StringProperty('')
    color = ListProperty(DEFAULT_COLOR)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global status
        status.bar = self