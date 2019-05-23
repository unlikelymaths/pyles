import multiprocessing
import pickle
import json
import importlib
from abc import ABC, abstractmethod
from os.path import join
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle

from data.image import Image, ImageLoadError

class IconLoadError(IOError):
    pass

def _info_path(dir_path):
    return join(dir_path, 'info.json')
    
class Icon(ABC, EventDispatcher):
    EMPTY = 0
    LOADING = 1
    FAILED = 2
    READY = 3
    MODIFIED = 4
    state = NumericProperty(EMPTY)
    
    def __init__(self, dir_path = None):
        super().__init__()
        self.dir_path = dir_path
        self._queue = None
        self._loader = None
        Clock.schedule_once(lambda dt: self.load())
        
    def load(self):
        """Load the icon asynchronously"""
        if self.state == Icon.EMPTY:
            self.state = Icon.LOADING
            self._queue = multiprocessing.Queue()
            target = self.__class__.load_data
            arguments = self.arguments()
            if isinstance(arguments,dict):
                args = (self._queue,)
                kwargs = arguments
            else:
                args = (self._queue,) + tuple(arguments)
                kwargs = {}
            self._loader = multiprocessing.Process(
                target=target, args=args, kwargs=kwargs, daemon=True)
            self._loader.start()   
            Clock.schedule_interval(lambda dt: self._check_load(), 0.01)
        
    def _check_load(self):
        if self._loader is not None and not self._queue.empty():
            success = self.copy_queue(self._queue)
            self._loader.join()
            self._queue = None
            self._loader = None
            if success:
                self.state = Icon.READY
            else:
                self.state = Icon.FAILED
        
    def save_as(self, file_path):
        """Saves the icon as image to file file_path"""
        self.get_image().save(file_path)
        
    def save(self, dir_path):
        data = {'__name__': self.__class__.__name__,
                '__module__': self.__class__.__module__}
        file_path = _info_path(dir_path)
        with open(file_path, 'w') as file:
            json.dump(data,file)
        self.save_data(dir_path)
            
    @abstractmethod
    def save_data(self, dir_path):
        """Saves the icons raw data to directory dir_path"""
        pass
        
    @abstractmethod
    def arguments(self):
        """Iterable or dict of arguments passed to load_data"""
        pass
    
    @abstractmethod
    def load_data(queue, *args, **kwargs):
        """Loads all necessary data into queue"""
        pass
    
    @abstractmethod
    def copy_queue(self, queue):
        """Copy the results from the queue and return success as True/False"""
        pass
            
    @abstractmethod
    def draw(self, pos, size):
        """draws the image within the rectangle defined by pos and size"""
        pass
        
    @abstractmethod
    def get_image(self):
        """Returns the final image for saving"""
        pass
    
# Loads an image and that's it
class ImageIcon(Icon):
    def __init__(self, *args, from_file_path = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._from_file_path = from_file_path
        self._image = None
        
    def arguments(self):
        return (self._from_file_path,)
    
    def load_data(queue, filename):
        try:
            data = {'image': Image(filename)}
        except ImageLoadError as e:
            data = {'error': e}
        queue.put(data)

    def copy_queue(self, queue):
        data = queue.get()
        if 'image' in data:
            self._image = data['image']
            return True
        elif 'error' in data:
            pass
        return False
            
    def draw(self, pos, size):
        if self._image is not None:
            Rectangle(texture=self._image.texture, pos=pos, size=size)
        
    def get_image(self):
        pass
        

# Loads an image, but only displays a quadratic subimage
class QuadraticIcon(ImageIcon):
    def __init__(self, *args, texture_pos = None, texture_size = None, **kwargs):
        super().__init__(*args, **kwargs)     
        self.texture_pos = texture_pos  
        self.texture_size = texture_size  
        self._texture_coordinates = None
        self._relpos = None
        self._relsize = None
    
    def save_data(self, dir_path):
        if self._image is not None:
            self._image.save(join(dir_path, 'original.png'))
        
    def arguments(self):
        if self.dir_path is not None:
            return (join(self.dir_path, 'original.png'),)
        return super().arguments()
        
    def copy_queue(self, queue):
        super().copy_queue(queue)
        if self._image is not None:
            short_edge = min(self._image.size)
            self.texture_size = (short_edge,short_edge)
            self.texture_pos = (self._image.size[0]/2 - self.texture_size[0]/2,
                                self._image.size[1]/2 - self.texture_size[1]/2)
            return True
        return False
        
    def draw(self, pos, size):
        if self._image is not None:
            aspect_ratio = size[0] / size[1]
            image_aspect_ration = 1
            if aspect_ratio > image_aspect_ration:
                draw_size = (size[1]* image_aspect_ration, size[1])
                draw_pos = (pos[0] + size[0]/2 - draw_size[0]/2, pos[1])
            else:
                draw_size = (size[0], size[0] / image_aspect_ration)
                draw_pos = (pos[0], pos[1] + size[1]/2 - draw_size[1]/2)
            Rectangle(texture=self._image.texture, pos=draw_pos, size=draw_size,
                tex_coords = self.texture_coordinates)
             
    def get_image(self):
        return self._image.image.crop(
            (self.texture_pos[0], 
             self.texture_pos[1], 
             self.texture_pos[0] + self.texture_size[0], 
             self.texture_pos[1] + self.texture_size[1]))
             
    @property
    def texture_coordinates(self):
        if self._texture_coordinates is None and self._image is not None:
            self._texture_coordinates = [self.relpos[0],
                                            1-self.relpos[1], 
                                        self.relpos[0]+self.relsize[0],
                                            1-self.relpos[1], 
                                        self.relpos[0]+self.relsize[0], 
                                            1-self.relpos[1]-self.relsize[1], 
                                        self.relpos[0],                 
                                            1-self.relpos[1]-self.relsize[1]]
        return self._texture_coordinates
            
    @property
    def relpos(self):
        if self._relpos is None and self._image is not None:
            self._relpos = (self.texture_pos[0] / self._image.size[0], 
                            self.texture_pos[1] / self._image.size[1])
        return self._relpos
        
    @property
    def relsize(self):
        if self._relsize is None and self._image is not None:
            self._relsize = (self.texture_size[0] / self._image.size[0], 
                             self.texture_size[1] / self._image.size[1])
        return self._relsize

# Default for drag n drop action
def from_file(file_path, quadtratic = False):
    """Load a QuadraticIcon from a single image file"""
    icon = QuadraticIcon(from_file_path = file_path)
    return icon
    
def from_save(dir_path):
    file_path = _info_path(dir_path)
    with open(file_path, 'r') as file:
        data = json.load(file)
    module = importlib.import_module(data['__module__'])
    cls = getattr(module, data['__name__'])
    return cls(dir_path=dir_path)
    return None