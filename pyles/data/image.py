import multiprocessing
import PIL
from array import array
from kivy.graphics.texture import Texture 
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.clock import Clock

class ImageLoadError(IOError):
    pass

def load_image_to_queue(filename, queue):
    try:
        #Load image file
        image = PIL.Image.open(filename)
        # Get rawdata from image
        buf = image.getdata()
        # Unpack tuples and form array
        buf = [int(val) for triple in buf for val in triple]
        arr = array('B', buf)
        queue.put({'image': image, 'arr': arr})
    except OSError:
        error = 'Cannot open image "{}".'.format(filename)
        queue.put({'error': error})
    
class Image(EventDispatcher):
    EMPTY = 0
    LOADING = 1
    FAILED = 2
    LOADED = 3
    state = NumericProperty(EMPTY)
    
    def __init__(self, filename, load_async = True, load_now = True):
        self.filename = filename
        self.load_async = load_async
        self._pil_image = None
        self._texture = None
        self._size = None
        self._queue = None
        self._loader = None
        if load_now:
            if load_async:
                Clock.schedule_once(lambda dt: self.load_image())
            else:
                self.load_image()
                
    def _check_image(self, _):
        if self._queue is not None and not self._queue.empty():
            queue_dct = self._queue.get()
            if 'image' and 'arr' in queue_dct:
                self._pil_image = queue_dct['image']
                self._arr = queue_dct['arr']
                self.state = Image.LOADED
            elif 'error':
                self._error = queue_dct['error']
                self.state = Image.FAILED
            self._loader.join()
            self._loader = None
            self._queue = None
            return False
            
    def load_image(self):
        if self.state == Image.EMPTY:
            self.state = Image.LOADING
            if self.load_async:
                self._queue = multiprocessing.Queue()
                self._loader = multiprocessing.Process(
                    target=load_image_to_queue, 
                    args=(self.filename,self._queue),
                    daemon=True)
                self._loader.start()   
                Clock.schedule_interval(self._check_image, 0.05)
            else:
                self._load_image()
                #self._check_image()
        
    @property
    def image(self):
        if self._pil_image is None:
            self.load_image()
        return self._pil_image
        
    @property
    def texture(self):
        if self._texture is None and self.image is not None:
            # Create a new texture and blit data
            self._texture = Texture.create(size=self.size)
            self._texture.blit_buffer(self._arr, colorfmt='rgb', bufferfmt='ubyte')
            self._texture.flip_vertical()
        return self._texture
    
    @property
    def size(self):
        if self._size is None and self.image is not None:
            self._size = self.image.size
        return self._size
    
    @property
    def aspect_ratio(self):
        return self.size[0] / self.size[1]
        