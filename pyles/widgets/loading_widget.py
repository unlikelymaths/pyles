from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Rotate
from data.image import Image
from kivy.clock import Clock

from resources.util import loading_path


class LoadingWidget(Widget):
    _image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rpm = 1
        self.max_size = 100
        self.pre_parent = None
        self.update_timer = None
        self.load_image()
        self.init_canvas()
        self.on_parent(self, self.parent)
        
    def init_canvas(self):
        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate(angle=0, origin=self.center)
        with self.canvas.after:
            PopMatrix()
        
    def load_image(self):
        if LoadingWidget._image is None:
            LoadingWidget._image = Image(loading_path)
        
    def on_parent(self, *args):
        # Remove from previous parent
        if self.pre_parent is not None:
            self.pre_parent.unbind(size=self.update_layout)
            self.pre_parent.unbind(pos=self.update_layout)
        self.pre_parent = self.parent
        
        # Register at new parent
        if self.parent is not None:
            self.parent.bind(size=self.update_layout)
            self.parent.bind(pos=self.update_layout)
            
        # Start timer or cancel old timer
        self.manage_update_timer()
        self.update_layout()
        
    def manage_update_timer(self):
        # Determine if clock should be active
        target = (self.parent is not None)
        
        # Cancel old clock
        if not target and self.update_timer is not None:
            self.update_timer.cancel()
            self.update_timer = None
        elif target and self.update_timer is None:
            self.update_timer = Clock.schedule_interval(self.update_angle, 0.01)
        
        
    def update_layout(self, *args):
        if self.parent is None:
            self.rect_pos = (0,0)
            self.rect_size = (0,0)
            self.rotation.origin = (0,0)
        else:
            width, height = self.parent.size
            short_edge = min((self.max_size, width / 2, height / 2))
            self.rect_size = (short_edge,short_edge)
            x,y = self.parent.pos
            x = x + 0.5 * (width - short_edge)
            y = y + 0.5 * (height - short_edge)
            self.rect_pos = (x,y)
            self.rotation.origin = self.parent.center
        self.draw()
            
    def update_angle(self, dt):
        self.rotation.angle = self.rotation.angle + dt * self.rpm * 360
        self.draw()
    
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            if self.parent is not None:
                pos = self.parent.pos
                size = self.parent.size
                Rectangle(texture=LoadingWidget._image.texture, 
                          pos = self.rect_pos, 
                          size = self.rect_size)