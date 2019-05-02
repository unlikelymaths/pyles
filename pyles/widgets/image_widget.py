from kivy.graphics import Rectangle
from kivy.properties import NumericProperty

from widgets.common import DropWidget
from data.image import Image, ImageLoadError

class ImageWidget(DropWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = None
        self.bind(size=self.size_callback)
        
    def size_callback(self, instance, value):
        self.draw()
    
    def draw(self):
        if self.image:
            aspect_ratio = self.width / self.height
            if aspect_ratio > self.image.aspect_ratio:
                size = (self.height * self.image.aspect_ratio, self.height)
                pos = (self.pos[0] + self.width/2 - size[0]/2, self.pos[1])
            else:
                size = (self.width, self.width / self.image.aspect_ratio)
                pos = (self.pos[0], self.pos[1] + self.height/2 - size[1]/2)
            with self.canvas:
                self.canvas.clear()
                Rectangle(texture=self.image.texture, pos=pos, size=size)
            
    def drop(self, file_path):
        accept_drop = False
        try:
            self.image = Image(file_path.decode('ascii'), load_now=True)
            accept_drop = True
        except ImageLoadError:
            self.image = None
            #TODO: Output error message to user
        self.draw()
        return accept_drop