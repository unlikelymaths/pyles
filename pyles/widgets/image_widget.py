from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from widgets.common import DropWidget
from data.image import Image, ImageLoadError
from data.imagesection import ImageSection

from widgets.util import widget_path
from widgets.loading_widget import LoadingWidget


Builder.load_file(widget_path('widgets/image_widget.kv'))

class ImageWidget(DropWidget):
    image = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.imagesection = None
        self.bind(size=self.layout_callback)
        self.bind(pos=self.layout_callback)
        
    def layout_callback(self, instance, value):
        self.draw()
            
    def draw(self):
        if self.image is not None:
            if self.image.state == Image.LOADED:
                aspect_ratio = self.width / self.height
                if aspect_ratio > self.imagesection.aspect_ratio:
                    size = (self.height * self.imagesection.aspect_ratio, self.height)
                    pos = (self.pos[0] + self.width/2 - size[0]/2, self.pos[1])
                else:
                    size = (self.width, self.width / self.imagesection.aspect_ratio)
                    pos = (self.pos[0], self.pos[1] + self.height/2 - size[1]/2)
                self.canvas.clear()
                with self.canvas:
                    Rectangle(texture=self.imagesection.texture, 
                            tex_coords=self.imagesection.tex_coords,
                            pos=pos, size=size)
        else:
            self.canvas.clear()
    
    def on_state(self, image, state):
        self.clear_widgets()
        if state == Image.LOADING:
            self.add_widget(LoadingWidget())
        elif state == Image.LOADED:
            self.image.texture
            short_edge = min(self.image.size)
            self.imagesection = ImageSection(self.image, size=(short_edge,short_edge))
        elif state == Image.FAILED:
            self.image = None
            self.imagesection = None
        self.draw()
            
    def load_entry(self, entry):
        self.canvas.clear()
        if entry.image is None:
            entry.image = Image(entry.icon_path)
        self.image = entry.image
        if self.image.state == Image.LOADED:
            self.on_state(self.image, self.image.state)
        else:
            self.on_state(self.image, self.image.state)
            self.image.bind(state=self.on_state)
    
    def load_file(self, file_path):
        self.canvas.clear()
        self.image = Image(file_path)
        self.image.bind(state=self.on_state)
    
    def drop(self, file_path):
        self.load_file(file_path)
        return True