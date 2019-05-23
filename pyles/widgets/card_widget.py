from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from resources.util import card_path
from data.image import Image

def coords(xmin,xmax,ymin,ymax):
    return [xmin,ymin, 
        xmax,ymin, 
        xmax,ymax, 
        xmin,ymax]
            
class CardWidget(Widget):
    _image = None
    _coordinates = [
        coords(0,1/3,0,1/3),     # Top Left
        coords(0,1/3,1/3,2/3),   # Left
        coords(0,1/3,2/3,3/3),   # Bottom Left
        coords(1/3,2/3,0,1/3),   # Top Center
        coords(1/3,2/3,1/3,2/3), # Center
        coords(1/3,2/3,2/3,3/3), # Bottom Center
        coords(2/3,1,0,1/3),     # Top Right
        coords(2/3,1,1/3,2/3),   # Right
        coords(2/3,1,2/3,3/3),   # Bottom Right
        ]
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border = 20
        self.load_image()
        self.bind(size=self.layout_callback)
        self.bind(pos=self.layout_callback)
        
    def load_image(self):
        if CardWidget._image is None:
            CardWidget._image = Image(card_path)

    def layout_callback(self, instance, value):
        self.positions = [
            (self.pos[0], self.pos[1]),
            (self.pos[0], self.pos[1] + self.border),
            (self.pos[0], self.pos[1] + self.size[1] - self.border),
            (self.pos[0] + self.border, self.pos[1]),
            (self.pos[0] + self.border, self.pos[1] + self.border),
            (self.pos[0] + self.border, self.pos[1] + self.size[1] - self.border),
            (self.pos[0] + self.size[0] - self.border, self.pos[1]),
            (self.pos[0] + self.size[0] - self.border, self.pos[1] + self.border),
            (self.pos[0] + self.size[0] - self.border, self.pos[1] + self.size[1] - self.border),
            ]
        self.sizes = [
            (self.border,self.border),
            (self.border,self.size[1] - 2 * self.border),
            (self.border,self.border),
            (self.size[0] - 2 * self.border, self.border),
            (self.size[0] - 2 * self.border, self.size[1] - 2 * self.border),
            (self.size[0] - 2 * self.border, self.border),
            (self.border,self.border),
            (self.border,self.size[1] - 2 * self.border),
            (self.border,self.border),
            ]
        for child in self.children:
            child.pos = (self.pos[0] + self.border,
                         self.pos[1] + self.border)
            child.size = (self.size[0] - 2 * self.border,
                          self.size[1] - 2 * self.border)
        self.draw()
            
    def draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            for i in range(9):
                pos = self.positions[i]
                size = self.sizes[i]
                coordinates = CardWidget._coordinates[i]
                Rectangle(texture = CardWidget._image.texture, 
                    tex_coords = coordinates,
                    pos = pos, size = size)