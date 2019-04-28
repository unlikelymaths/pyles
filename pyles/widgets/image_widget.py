from kivy.graphics import Rectangle

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
            with self.canvas:
                self.canvas.clear()
                Rectangle(texture=self.image.texture, pos=self.pos, size=(self.width, self.height))
            
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