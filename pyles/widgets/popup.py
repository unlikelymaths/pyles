import weakref
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.popup  import Popup
from kivy.properties import StringProperty
from kivy.lang import Builder

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/popup.kv'))


class PopupWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None

    def set_popup(self, popup):
        self.popup = weakref.proxy(popup)

class NotificationWidget(PopupWidget):
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get('text', '')
    
    def on_close(self):
        if self.popup:
            self.popup.dismiss()

class QuestionWidget(PopupWidget):
    text = StringProperty()

    def __init__(self, on_yes, on_no, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get('text', '')
        if on_yes == False:
            self.alternatives.remove_widget(self.yes_button)
        elif callable(on_yes):
            self.yes_button.bind(on_press=lambda _: on_yes())
        if on_no == False:
            self.alternatives.remove_widget(self.no_button)
        elif callable(on_no):
            self.yes_button.bind(on_press=lambda _: on_no())
    
    def on_close(self):
        if self.popup:
            self.popup.dismiss()

def notification(title='Notification', text=''):
    content = NotificationWidget(text=text)
    popup = Popup(title=title,
        content=content,
        size_hint=(None, None), size=(400, 400))
    content.set_popup(popup)
    popup.open()

def question_dialog(title='Notification', text='', on_yes=False, on_no=False):
    content = QuestionWidget(on_yes, on_no, text=text)
    popup = Popup(title=title,
        content=content,
        size_hint=(None, None), size=(400, 300))
    content.set_popup(popup)
    popup.open()