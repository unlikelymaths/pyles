from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.lang import Builder

from widgets.common import DropWidget
from data.image import Image, ImageLoadError
from data.imagesection import ImageSection

from widgets.util import widget_path

Builder.load_file(widget_path('widgets/image_widget.kv'))

class ImageWidget(DropWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = None
        self.imagesection = None
        self.bind(size=self.size_callback)
        
    def size_callback(self, instance, value):
        self.draw()
    
    def draw(self):
        if self.imagesection:
            aspect_ratio = self.width / self.height
            if aspect_ratio > self.imagesection.aspect_ratio:
                size = (self.height * self.imagesection.aspect_ratio, self.height)
                pos = (self.pos[0] + self.width/2 - size[0]/2, self.pos[1])
            else:
                size = (self.width, self.width / self.imagesection.aspect_ratio)
                pos = (self.pos[0], self.pos[1] + self.height/2 - size[1]/2)
            with self.canvas:
                self.canvas.clear()
                Rectangle(texture=self.imagesection.texture, 
                          tex_coords=self.imagesection.tex_coords,
                          pos=pos, size=size)
            
    def load_file(self, file_path):
        try:
            self.image = Image(file_path, load_now=True)
            short_edge = min(self.image.size)
            self.imagesection = ImageSection(self.image, size=(short_edge,short_edge))
            print(self.imagesection.tex_coords)
        except ImageLoadError as e:
            self.image = None
            self.imagesection = None
            raise e
            #TODO: Output error message to user
    
    def drop(self, file_path):
        accept_drop = False
        try:
            self.load_file(file_path)
            accept_drop = True
        except ImageLoadError:
            pass
        self.draw()
        return accept_drop